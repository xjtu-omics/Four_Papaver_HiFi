import os
import pandas as pd
import numpy as np
import argparse
def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-t", "--trf_dir")
    parser.add_argument("-c", "--chrnumber",type=int)
    parser.add_argument("-o", "--outdir")
    args = parser.parse_args()
    TRF_dir = args.trf_dir
    outdir = args.outdir

    chrnumber = args.chrnumber

    # TRF_dir = 'G:/Papaver/DCW/DCW_TRF'
    # outdir = 'G:/Papaver/DCW/testOUT'
    #
    # chrnumber = 22

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    min_f = 100
    min_len = 100
    name_list_file = outdir + '/namelist.txt'
    name_list_file = open(name_list_file, 'w')
    name_list = []
    for i in range(chrnumber):
        file_name = TRF_dir + '/' + 'chr'+str(i+1)+'.fa.2.7.7.80.10.50.500.2.xls'
        chr = 'chr'+str(i+1)
        print(chr)
        trf = pd.read_csv(file_name,sep='\t',header=None)[[0,1,2,3,13]]
        trf = trf.loc[(trf[2] > min_len) & (trf[3] > min_f)]
        trf.columns = ['start', 'end', 'RUL', 'RN', 'RU']
        # 区间完全一样保留单元小的
        trf = np.asarray(trf)
        regions = {}
        for j in trf:
            key = str(j[0]) + '_' + str(j[1])
            if key not in regions.keys():
                regions[key] = j
            else:
                if regions[key][2] > j[2]:
                    regions[key] = j

        for j in regions.keys():
            name = chr + '_' + str(regions[j][0]) + '_' + str(regions[j][1]) + '_' + str(regions[j][2])
            outfile = outdir + '/' + name + '.fa'
            outfile = open(outfile,'w')
            name_list_file.write(chr+'\t'+name + '\n')
            name_list.append([chr,name])
            seq = regions[j][4]

            outfile.write('>' + name + '\n')
            outfile.write(seq + '\n')
            outfile.close()




if __name__ == '__main__':
    main()