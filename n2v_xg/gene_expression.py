import numpy as np
import os
import sys

filename = sys.argv[1]

if os.path.isfile('hs_eppugnn_ge-feats.npy'):
    os.remove('hs_eppugnn_ge-feats.npy')

id_map_rev = {}
with open(filename, 'r') as f:
    i = 0
    f.readline()
    for line in f:
        line = line.strip().split(' ')
        id_map_rev[int(line[0])] = i
        i += 1

id_map = {v: k for k, v in id_map_rev.items()}
id_bioname_dict = {}

with open('BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_bioname_dict[line[1]] = line[7]
        id_bioname_dict[line[2]] = line[8]

ge_matrix = np.zeros((len(id_map), 1558), dtype=np.float64)
name_index = {id_bioname_dict[str(id_map[v])] : v  for v in id_map.keys() }

with open('../data/GSE86354_GTEx_FPKM_gene.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

np.save('hs_eppugnn_ge-feats.npy', ge_matrix)

# b = np.load('hs_eppugnn_ge-feats.npy')
# a = np.load('hs_eppugnn_sl-feats.npy')

# c = np.concatenate((a, b), axis=1)
# print(c.shape)
# np.save('hs_eppugnn-feats.npy', c)