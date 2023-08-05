import argparse

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--name_list_file")
    parser.add_argument("-w", "--work_dir")
    args = parser.parse_args()

    name_list_file = args.name_list_file
    work_dir = args.work_dir

    with open(name_list_file,'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            name = line.split('\t')[1]
            print(name)
            sd_file = work_dir + '/' + name + '/final_decomposition.tsv'
            out_continue_region_file = work_dir + '/' + name + '/continue_region.txt'
            print(sd_file)
            continuous_region = []
            region = []
            with open(sd_file,'r') as sf:
                while True:
                    line = sf.readline()[:-1]
                    if not line:
                        break
                    items = line.split('\t')
                    start = int(items[2])
                    end = int(items[3])
                    identity = float(items[4])
                    if identity < 80:
                        continue
                    region.append([start,end])

            if len(region) == 1:
                continuous_region.append(region[0])
            else:
                init_region = region[0]
                for i in range(len(region) - 1):
                    if region[i+1][0] - init_region[1] == 1:
                        init_region[1] = region[i + 1][1]
                    else:
                        continuous_region.append(init_region)
                        init_region = region[i+1]
                continuous_region.append(init_region)
            out_continue_region_file = open(out_continue_region_file,'w')
            for i in continuous_region:
                out_continue_region_file.write(str(i[0])+'\t' + str(i[1])+'\n')
            out_continue_region_file.close()




if __name__ == '__main__':
    main()