import argparse

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--name_list_file")
    parser.add_argument("-w", "--work_dir")
    args = parser.parse_args()

    name_list_file = args.name_list_file
    work_dir = args.work_dir

    # name_list_file = 'G:/Papaver/V4/namelist.txt'
    # work_dir = 'G:/Papaver/V4'

    name_list = {}
    with open(name_list_file,'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            name = line.split('\t')[1]
            name_info = name.split('_')
            chr = name_info[0]
            start = int(name_info[1])
            end = int(name_info[2])
            unit_len = int(name_info[3])
            if chr not in name_list.keys():
                name_list[chr] = [[start,end,unit_len]]
            else:
                name_list[chr].append([start,end,unit_len])

    filter_name_list = {}
    for i in name_list.keys():
        chr = i
        filter_name_list[chr] = []
        sorted_region = sorted(name_list[chr],key=lambda x:x[0])
        start_one = sorted_region[0]
        
        for j in range(len(sorted_region) - 1):
            index = j + 1
            if start_one[1] >= sorted_region[index][0]:
                
                overlap = start_one[1] - sorted_region[index][0]
                if overlap / (sorted_region[index][1] - sorted_region[index][0]) > 0.8:
                    
                    if start_one[2] > sorted_region[index][2]:
                        start_one = sorted_region[index]
                    else:
                        start_one = start_one
                else:
                    filter_name_list[chr].append(start_one)
                    start_one = sorted_region[index]
            else:
                filter_name_list[chr].append(start_one)
                start_one = sorted_region[index]

        filter_name_list[chr].append(start_one)

    outfile = work_dir + '/namelist.filter.txt'
    outfile = open(outfile,'w')
    for i in filter_name_list.keys():
        for j in filter_name_list[i]:
            outfile.write(i+'\t'+i+'_'+str(j[0]) +'_'+str(j[1]) + '_'+str(j[2])+'\n')
    outfile.close()








if __name__ == '__main__':
    main()
