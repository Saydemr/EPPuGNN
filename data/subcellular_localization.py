import numpy as np
from sklearn import decomposition as dc 
import json

locations = ['Nucleus', 'Cytosol', 'Cytoskeleton', 'Peroxisome', 'Vacuole', 'Endoplasmic reticulum', 'Golgi apparatus', 'Plasma membrane', 'Endosome', 'Extracellular space', 'Mitochondrion'] 

id_map = json.load(open('hs_eppugnn-id_map_inv.json'))
id_name_dict ={}

with open('BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_name_dict[line[1]] = line[7]
        id_name_dict[line[2]] = line[8]

name_index = {id_name_dict[str(id_map[v])] : v  for v in id_map.keys() }

sl_matrix = np.zeros((len(id_map), 11), dtype=np.float64)

with open('human_compartment_knowledge_full.tsv', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[1]
        sl_feature = line[3]
        if name not in name_index.keys() or sl_feature not in locations:
            continue
        index = int(name_index[name])
        sl_matrix[index, locations.index(sl_feature)] = 1

print(sl_matrix.sum(axis=0))
np.save('hs_eppugnn_sl-feats.npy', sl_matrix)
