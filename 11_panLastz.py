import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-w", "--work_dir")
    parser.add_argument("-o", "--out_dir")
    parser.add_argument("-s", "--split_ref_dir")

    args = parser.parse_args()
    lastz_path = '/opt/anaconda2/bin/lastz'
    sp_list = {'YMR':7,'PB':7,'HN1':11,'DCW':22}
    work_dir = args.work_dir
    out_dir = args.out_dir
    split_ref_dir = args.split_ref_dir
    namelist = []
    for i in sp_list.keys():
        community_file = work_dir + '/' + i +'/community.xls'
        with open(community_file,'r') as cf:
            while True:
                line = cf.readline()[:-1]
                if not line:
                    break
                items = line.split('\t')
                namelist.append(i+'@'+items[0])

    for i in namelist:
        print(i)
        info = i.split('@')
        out_lastz_dir = out_dir + '/' + i
        if not os.path.exists(out_lastz_dir):
            os.mkdir(out_lastz_dir)
        target_fa = work_dir +'/' + info[0] + '/' + info[1] + '.fa'
        for j in sp_list.keys():
            for k in range(sp_list[j]):
                ref = split_ref_dir +'/' +j+ '/chr' + str(k + 1) + '.fa'
                cmd = lastz_path + ' ' + ref + ' ' + target_fa + ' ' + \
                      '--format=general:score,name1,strand1,size1,start1,' \
                      'end1,name2,strand2,identity,' \
                      'length1,align1' + ' > ' + out_lastz_dir + '/'+j+'_'+'chr' + str(k + 1) + '.xls'
                os.system(cmd)


if __name__ == '__main__':
    main()
