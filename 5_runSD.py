import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--name_list_file")
    parser.add_argument("-r", "--ref_path")
    parser.add_argument("-w", "--work_dir")
    args = parser.parse_args()

    name_list_file = args.name_list_file
    ref_path = args.ref_path
    work_dir = args.work_dir

    sd_path = '/home/shgao/home/soft/stringdecomposer-master/bin/stringdecomposer'
    samtools_path = '/home/xfyang/software/miniconda3/bin/samtools'
    python_path = '/home/shgao/.conda/envs/SCAT/bin/python'

    with open(name_list_file,'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            items = line.split('\t')
            chr = items[0]
            start = items[1].split('_')[1]
            end = items[1].split('_')[2]
            # 先创建路径
            out_sd_dir = work_dir + '/' + items[1]
            if not os.path.exists(out_sd_dir):
                os.mkdir(out_sd_dir)
            # samtools
            cmd = samtools_path + ' ' + 'faidx' + ' ' + ref_path + ' ' + chr+':'+start+'-'+end + ' ' + '>' + out_sd_dir+'/'+items[1]+'.fa'

            os.system(cmd)
            # sd
            cmd = python_path + ' ' + sd_path + ' ' + out_sd_dir+'/'+items[1]+'.fa' + ' ' + work_dir+'/'+items[1]+'.fa' + ' ' + '-o' + ' ' + out_sd_dir

            os.system(cmd)




if __name__ == '__main__':
    main()