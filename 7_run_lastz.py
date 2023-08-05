import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--name_list_file")
    parser.add_argument("-s", "--split_ref_dir")
    parser.add_argument("-c", "--chr_number",type=int)
    parser.add_argument("-w", "--work_dir")

    args = parser.parse_args()

    name_list_file = args.name_list_file
    split_ref_dir = args.split_ref_dir
    chr_number = args.chr_number
    work_dir = args.work_dir

    lastz_path = '/opt/anaconda2/bin/lastz'

    with open(name_list_file,'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            name = line.split('\t')[1]
            out_lastz_dir = work_dir + '/' + name
            if not os.path.exists(out_lastz_dir):
                os.mkdir(out_lastz_dir)
            target_fa = work_dir + '/' + name +'.fa'
            print(target_fa)
            for i in range(chr_number):
                ref = split_ref_dir + '/chr' + str(i+1) + '.fa'
                cmd = lastz_path + ' ' + ref + ' ' + target_fa + ' ' + \
                      '--format=general:score,name1,strand1,size1,start1,' \
                      'end1,name2,strand2,identity,' \
                      'length1,align1' + ' > ' + out_lastz_dir +'/chr'+str(i+1)+'.xls'
                os.system(cmd)


if __name__ == '__main__':
    main()