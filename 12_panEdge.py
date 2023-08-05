import networkx as nx
import pandas as pd
import argparse
import os
import networkx.algorithms.community as nx_comm
def main():
    # 10. 建立edge，条件，cov80，identity80, 建立edge
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-w", "--workdir")
    parser.add_argument("-o", "--outdir")
    sp_list = {'DCW': 22,'HN1':11, 'YMR': 7, 'PB': 7}

    args = parser.parse_args()
    work_dir = args.workdir
    outdir = args.outdir
    namelist = []
    for i in sp_list.keys():
        community_file = work_dir + '/' + i + '/community.xls'
        with open(community_file, 'r') as cf:
            while True:
                line = cf.readline()[:-1]
                if not line:
                    break
                items = line.split('\t')
                namelist.append(i + '@' + items[0])

    print('start process')

    name_info_table = {}
    for i in namelist:
        info = i.split('@')
        sd_continue_file = work_dir + '/' + info[0] + '/' + info[1] + '/continue_region.txt'
        sd_continue = []
        with open(sd_continue_file,'r') as sf:
            while True:
                line = sf.readline()[:-1]
                if not line:
                    break
                items = line.split('\t')
                sd_continue.append([int(items[0]),int(items[1])])
        items = info[1].split('_')
        sp = info[0]
        chr = items[0]
        start = int(items[1])
        end = int(items[2])
        unit_len = int(items[3])

        if sp not in name_info_table.keys():
            name_info_table[sp] = {}
            name_info_table[sp][chr] = {}
            name_info_table[sp][chr][i] = [sp,chr, start, end, unit_len,sd_continue]
        else:
            if chr not in name_info_table[sp].keys():
                name_info_table[sp][chr] = {}
                name_info_table[sp][chr][i] = [sp, chr, start, end, unit_len, sd_continue]
            else:
                name_info_table[sp][chr][i] = [sp, chr, start, end, unit_len, sd_continue]

    edge_set = set()
    # 筛选条件，cov超过80%，且identity超过80
    count = 0
    print('start run')
    for i in namelist:
        print(i)
        lastz_dir = outdir + '/' + i
        name_info = (i.split('@'))[1].split('_')
        name_lastz_set = set()
        for j in sp_list.keys():
            for k in range(sp_list[j]):
                lastz_chr_file = lastz_dir + '/'+j+'_'+'chr' + str(k + 1) + '.xls'
                with open(lastz_chr_file, 'r') as lcf:
                    while True:
                        line = lcf.readline()[:-1]
                        if not line:
                            break
                        if line.startswith('#'):
                            continue
                        items = line.split('\t')
                        l_chr = items[1]
                        l_start = int(items[4])
                        l_end = int(items[5])
                        l_cov = int(items[8].split('/')[-1])
                        l_identity = float(items[9][:-1])
                        if l_cov < int(name_info[-1]) * 0.8:
                            continue
                        if l_identity < 80:
                            continue
                        # 其他情况判断与node的关系
                        if j not in name_info_table.keys():
                            continue
                        if l_chr not in name_info_table[j].keys():
                            continue
                        for l in name_info_table[j][l_chr].keys():
                            # 遍历区间看是否在其中
                            sd_continue = name_info_table[j][l_chr][l][5]
                            find = 0
                            name_info_k_start = int(name_info_table[j][l_chr][l][2])
                            for m in sd_continue:
                                n_start = name_info_k_start + int(m[0])
                                n_end = name_info_k_start + int(m[1])
                                if n_start < l_start and l_end < n_end:
                                    find = 1
                                    name_lastz_set.add(l)
                                    break
                            if find == 1:
                                break
        for j in name_lastz_set:
            if j == i:
                continue
            if (i+'$'+j in edge_set) or (j+'$'+i in edge_set):
                continue
            else:
                edge_set.add(i+'$'+j)
        count += 1
    edge_file = outdir + '/pan_edge.all.txt'
    edge_file = open(edge_file, 'w')
    for i in edge_set:
        edge_file.write(i + '\n')
    edge_file.close()

    G = nx.Graph()
    for i in edge_set:
        items = i.split('$')
        G.add_edge(items[0], items[1])

    community = nx_comm.louvain_communities(G, seed=1)

    community_set = set()
    for i in community:
        for j in i:
            community_set.add(j)

    outfile = outdir + '/pan_community.all.xls'
    outfile = open(outfile, 'w')
    for i in list(community):
        # 找度大的节点作为community name，统计community信息：重复单元长度，整个community存在的物种及覆盖
        region_number = len(i)
        unit_table = {}
        for j in i:
            items = j.split('_')
            unit_len = int(items[-1])
            if unit_len not in unit_table.keys():
                unit_table[unit_len] = 1
            else:
                unit_table[unit_len] += 1
        max_degree = -1
        max_degree_name = ''
        max_unit_len = -1
        max_unit = -1
        for j in unit_table.keys():
            if max_unit_len < unit_table[j]:
                max_unit_len = unit_table[j]
                max_unit = j
        for j in i:
            items = j.split('_')
            unit_len = int(items[-1])

            if unit_len == max_unit:

                if G.degree(j) > max_degree:
                    max_degree = G.degree(j)
                    max_degree_name = j

        outfile.write(max_degree_name)

        outfile.write('\t' + str(max_unit))
        outfile.write('\t' + str(region_number))
        for j in i:
            outfile.write('\t' + j)

        outfile.write('\n')

    for i in namelist:
        if i in community_set:
            continue
        outfile.write(i)
        info = i.split('_')
        unit_len = int(info[-1])
        region_number = 1
        outfile.write('\t' + str(unit_len))
        outfile.write('\t' + str(region_number))
        outfile.write('\t' + i)
        outfile.write('\n')


    outfile.close()




if __name__ == '__main__':
    main()
