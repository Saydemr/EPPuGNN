import json
import numpy as np
import os


id_bioname_dict = {}
nhi2gene = {}

with open('BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_bioname_dict[line[3]] = line[7]
        id_bioname_dict[line[4]] = line[8]

bioname_id_dict = {v: k for k, v in id_bioname_dict.items()}


with open('GPL570-55999.txt', 'r') as f:
    for line in f:
        if line.startswith('#') or line.startswith('ID'):
            continue
        line = line.strip().split('\t')
        
        if "///" in line[10]:
            genes = line[10].strip().split("///")

            if genes[0] in bioname_id_dict.keys():
                nhi2gene[line[0]] = genes[0]
            else:
                nhi2gene[line[1]] = genes[0]
        else:
            nhi2gene[line[0]] = line[10]


with open('GSE3431_series_matrix.txt', 'r') as f:
    with open('GSE3431_series_matrix_gene.txt', 'w+') as g:
        for line in f:
            line = line.strip()
            if line.startswith('!') or line.startswith('"ID_REF"'):
                continue
            line = line.split('\t')
            check = line[0].replace("\"","")

            if check in nhi2gene:
                if nhi2gene[check] == "":
                    continue
                g.write(nhi2gene[check] + '\t' + '\t'.join(line[1:]) + '\n')


id_map = json.load(open('hs_eppugnn-id_map_inv.json'))

ge_matrix = np.zeros((len(id_map), 36))

name_index = {id_bioname_dict[str(id_map[v])] : v  for v in id_map.keys() }

with open('GSE3431_series_matrix_gene.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

np.save('eppugnn_ge-feats.npy', ge_matrix)
os.remove('GSE3431_series_matrix_gene.txt')