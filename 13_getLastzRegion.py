import argparse


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-sr", "--select_region_file")
    parser.add_argument("-w", "--workdir")
    parser.add_argument("-sp", "--species")
    parser.add_argument("-c", "--chr_number", type=int)
    parser.add_argument("-o", "--outfile")

    args = parser.parse_args()

    select_region_file = args.select_region_file
    workdir = args.workdir
    species = args.species
    chr_number = args.chr_number
    outfile = args.outfile

    select_region = []
    with open(select_region_file,'r') as srf:
        while True:
            line = srf.readline()[:-1]
            if not line:
                break
            items = line.split('\t')
            select_region.append(items[0])

    final_bed = {}
    for i in select_region:
        lastz_dir = workdir + '/' + species +'/' + i
        unit_len = int(i.split('_')[-1])
        final_bed[i] = []
        for j in range(chr_number):
            chr = 'chr' + str(j+1)
            lastz_file = lastz_dir + '/' + chr +'.xls'
            with open(lastz_file, 'r') as lf:
                lf.readline()
                while True:
                    line = lf.readline()[:-1]
                    if not line:
                        break
                    items = line.split('\t')
                    start = int(items[4])
                    end = int(items[5])
                    cov = int(items[8].split('/')[-1])
                    identity = float(items[9][:-1])
                    if cov / unit_len < 0.8:
                        continue
                    if identity < 80:
                        continue
                    final_bed[i].append([chr, start, end])
    outfile = open(outfile,'w')
    for i in final_bed.keys():
        for j in final_bed[i]:
            outfile.write(i +'\t' +  j[0]+'_'+str(j[1])+'_'+str(j[2]) + '\n')
    outfile.close()


if __name__ == '__main__':
    main()