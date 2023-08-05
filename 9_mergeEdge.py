import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
import argparse
def main():
    # 8.生成图创建 community
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-w", "--work_dir")
    parser.add_argument("-n", "--name_list_file")

    args = parser.parse_args()
    work_dir = args.work_dir
    name_list_file = args.name_list_file

    name_list = []
    with open(name_list_file, 'r') as nlf:
        while True:
            line = nlf.readline()[:-1]
            if not line:
                break
            items = line.split('\t')
            name_list.append(items[1])

    edge_set = set()
    for i in range(28):
        print(i)
        edge_file = work_dir + '/' + 'con_edge.80.80.'+str(i+1)+'.txt'
        with open(edge_file, 'r') as ef:
            while True:
                line = ef.readline()[:-1]
                if not line:
                    break
                items = line.split('$')
                if line in edge_set:
                    continue
                if items[1]+'$'+items[0] in edge_set:
                    continue
                edge_set.add(line)
    outedgefile = work_dir + '/edge.xls'
    outedgefile = open(outedgefile, 'w')
    G = nx.Graph()
    for i in edge_set:
        items = i.split('$')
        G.add_edge(items[0],items[1])
        outedgefile.write(i+'\n')
    outedgefile.close()


    community = nx_comm.louvain_communities(G, seed=1)

    community_set = set()
    for i in community:
        for j in i:
            community_set.add(j)

    outfile = work_dir + '/community.xls'
    outfile = open(outfile,'w')
    for i in list(community):
        # 找unit_len最多的中度大的节点作为community name
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
        outfile.write('\t'+str(max_unit))
        outfile.write('\t' + str(region_number))
        for j in i:
            outfile.write('\t' + j)
        outfile.write('\n')

    for i in name_list:
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