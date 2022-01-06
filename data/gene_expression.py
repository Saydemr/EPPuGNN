import json
import numpy as np
import os
import scipy as sp
from scipy import sparse
from sklearn.decomposition import PCA

id_bioname_dict = {}
nhi2gene = {}

with open('BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        id_bioname_dict[line[1]] = line[7]
        id_bioname_dict[line[2]] = line[8]

bioname_id_dict = {v: k for k, v in id_bioname_dict.items()}

with open('GPL570-55999.txt', 'r') as f:
    for line in f:
        if line.startswith('#') or line.startswith('ID'):
            continue
        line = line.strip().split('\t')
    
        if len(line) < 10:
            continue

        if "///" in line[10]:
            genes = line[10].strip().split("///")

            if genes[0] in bioname_id_dict.keys():
                nhi2gene[line[0]] = genes[0]
            else:
                nhi2gene[line[0]] = genes[1]
        else:
            nhi2gene[line[0]] = line[10]


nhi2gene_inv = {v: k for k, v in nhi2gene.items()}

with open('GSE86354_GTEx_FPKM.txt', 'r') as f:
    with open('GSE86354_GTEx_FPKM_gene.txt', 'w+') as g:
        for line in f:
            line = line.strip().split('\t')
            check = line[0]
            if check in nhi2gene_inv.keys():

                if nhi2gene_inv[check] == "":
                    continue
                g.write(check + '\t' + '\t'.join(line[1:]) + '\n')

id_map = json.load(open('hs_eppugnn-id_map_inv.json'))
ge_matrix = np.zeros((len(id_map), 1558), dtype=np.float64)
name_index = {id_bioname_dict[str(id_map[v])] : v  for v in id_map.keys() }

with open('GSE86354_GTEx_FPKM_gene.txt', 'r') as f:
    for line in f:
        line = line.strip().split('\t')
        name = line[0]
        ge_vector = line[1:]
        if name not in name_index.keys():
            continue
        
        index = int(name_index[name])
        ge_matrix[index] = ge_vector

print(ge_matrix.shape)

pca = PCA(n_components=0.975)
pca.fit(ge_matrix)

# print(pca.components_)
# print(pca.explained_variance_ratio_)
print(np.sum(pca.explained_variance_ratio_))
print(len(pca.explained_variance_ratio_))
# transform data
ge_matrix = pca.transform(ge_matrix)
print(ge_matrix.shape)

np.save('hs_eppugnn_ge-feats.npy', ge_matrix)

b = np.load('hs_eppugnn_ge-feats.npy',allow_pickle=True,fix_imports=True)
a = np.load('hs_eppugnn_sl-feats.npy',allow_pickle=True,fix_imports=True)

c = np.concatenate((a, b), axis=1)
np.save('hs_eppugnn_ge-sl-feats.npy', c)
sp.sparse.save_npz('../grand_blend/hs_eppugnn-feats.npz', sparse.csr_matrix(c))