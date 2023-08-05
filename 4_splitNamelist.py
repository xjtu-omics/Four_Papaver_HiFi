import argparse

def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-n", "--name_list_file")
    parser.add_argument("-o", "--out_dir")
    args = parser.parse_args()

    name_list_file = args.name_list_file
    out_dir = args.out_dir
    #
    # name_list_file = 'G:/Papaver/DCW/testOUT/namelist.txt'
    # out_dir = 'G:/Papaver/DCW/testOUT'
    line_list = []
    with open(name_list_file, 'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            line_list.append(line)

        # 分割namelist

    split_number = 28
    one_file = int(len(line_list) / split_number) + 1
    for i in range(split_number):
        outfile = out_dir + '/namelist' + '.' + str(i + 1) + '.txt'
        split_name_list = line_list[i * one_file:i * one_file + one_file]
        outfile = open(outfile, 'w')
        for j in split_name_list:
            outfile.write(j+ '\n')
        outfile.close()





if __name__ == '__main__':
    main()