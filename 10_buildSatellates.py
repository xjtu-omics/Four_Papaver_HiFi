import argparse


def main():
    # stat satellite information
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-cf", "--communities_file")
    parser.add_argument("-w", "--workdir")
    parser.add_argument("-sp", "--species")
    parser.add_argument("-c", "--chr_number", type=int)
    parser.add_argument("-g", "--genome_size", type=int)
    parser.add_argument("-o", "--outfile")

    args = parser.parse_args()

    communities_file = args.communities_file
    workdir = args.workdir
    species = args.species
    chr_number = args.chr_number
    genome_size = args.genome_size
    outfile = args.outfile
    outfile = open(outfile,'w')
    outfile.write('Satellites'+'\t' + 'Represented_Region' +'\t' +'Length'+'\t'+'Chromosomes'+'\t'+
                  'AT_Percentage'+'\t'+'Repeat_Number'+'\t' + 'Genomic_Percentage'+'\t'+
                  'Genomic_Size'+'\t'+'Sequence'+'\n')

    satellites = []
    with open(communities_file,'r') as cf:
        while True:
            line = cf.readline()[:-1]
            if not line:
                break
            items = line.split('\t')
            target_region = items[0]
            unit_len = int(items[1])
            lastz_dir = workdir + '/' + items[0]
            motif_file = workdir + '/' + items[0] +'.fa'
            motif_seq = ''
            with open(motif_file,'r') as mf:
                mf.readline()
                motif_seq = mf.readline()[:-1]
            AT_ratio = 0
            for i in motif_seq:
                if i == 'A' or i == 'T':
                    AT_ratio += 1
            AT_ratio = round(AT_ratio / len(motif_seq), 4) * 100
            bed = []
            for i in range(chr_number):
                lastz_file = lastz_dir + '/chr' + str(i + 1) + '.xls'
                with open(lastz_file,'r') as lf:
                    lf.readline()
                    while True:
                        line = lf.readline()[:-1]
                        if not line:
                            break
                        items = line.split('\t')
                        chr = 'chr' + str(i + 1)
                        start = int(items[4])
                        end = int(items[5])
                        cov = int(items[8].split('/')[-1])
                        identity = float(items[9][:-1])
                        if cov / unit_len < 0.8:
                            continue
                        if identity < 80:
                            continue
                        bed.append([chr,start,end])
            chr_bed = {}
            for i in bed:
                if i[0] not in chr_bed.keys():
                    chr_bed[i[0]] = [[i[1],i[2]]]
                else:
                    chr_bed[i[0]].append([i[1],i[2]])
            repeat_number = len(bed)
            genome_content = 0
            for i in bed:
                genome_content += (i[2] - i[1])
            genomic_percentage = round(genome_content / genome_size, 4) * 100
            chrs = ''
            for i in chr_bed.keys():
                chrs += i +','
            chrs = chrs[:-1]

            # outfile.write(name+'\t'+target_region+'\t'+str(unit_len)+'\t'+chrs+'\t'+
            #               str(AT_ratio)+'%'+'\t'+str(repeat_number)+'\t'+str(genomic_percentage)+'%'+'\t'+
            #               str(genome_content)+'\t'+motif_seq+'\n')
            satellites.append([target_region,unit_len,chrs,AT_ratio,repeat_number,
                               genomic_percentage,genome_content,motif_seq])
    satellites = sorted(satellites,key=lambda x:x[3],reverse=True)
    name_index = 1
    for i in satellites:
        target_region = i[0]
        unit_len = i[1]
        chrs = i[2]
        AT_ratio = i[3]
        repeat_number = i[4]
        genomic_percentage = i[5]
        genome_content = i[6]
        motif_seq = i[7]
        name = species + str(unit_len)+'S'+str(name_index)

        outfile.write(name+'\t'+target_region+'\t'+str(unit_len)+'\t'+chrs+'\t'+
                      str(AT_ratio)+'%'+'\t'+str(repeat_number)+'\t'+str(genomic_percentage)+'%'+'\t'+
                      str(genome_content)+'\t'+motif_seq+'\n')
        name_index += 1
    outfile.close()






if __name__ == '__main__':
    main()
