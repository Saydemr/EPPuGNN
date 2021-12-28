from os import sep
import networkx as nx
from networkx.readwrite import json_graph
from random import choices
from collections import Counter
import json
import numpy as np


print("Loading graph...")
ppi_graph = nx.Graph() 

id_map = {}
id_map_int = {}
id_map_inv = {}
id_map_inv_int = {}

with open("BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt") as f:
    f.readline()
    i = 0
    for line in f:
        
        line = line.strip()
        line = line.split("\t")

        if line[1] == line[2]:
            continue
    
        if not line[1].isdigit() or not line[2].isdigit():
            continue
        if int(line[1]) not in id_map_int and int(line[2]) not in id_map_int:
            ppi_graph.add_edge(i,i+1)

            id_map[line[1]] = i
            id_map_int[int(line[1])] = i
            id_map_inv[i] = line[1]
            id_map_inv_int[i] = int(line[1])
            ppi_graph.nodes[i]['id'] = i

            id_map[line[2]] = i+1
            id_map_int[int(line[2])] = i+1
            id_map_inv[i+1] = line[2]
            id_map_inv_int[i+1] = int(line[2])
            ppi_graph.nodes[i+1]['id'] = i+1
            
            #print(i, i+1)
            i+=2

        elif int(line[1]) in id_map_int and int(line[2]) not in id_map_int:
            
            ppi_graph.add_edge(id_map_int[int(line[1])],i)

            id_map[line[2]] = i
            id_map_int[int(line[2])] = i
            id_map_inv[i] = line[2]
            id_map_inv_int[i] = int(line[2])

            ppi_graph.nodes[i]['id'] = i
            #print(id_map_int[int(line[1])], i)
            i+=1

            
        elif int(line[1]) not in id_map_int and int(line[2]) in id_map_int:
            
            ppi_graph.add_edge(i,id_map_int[int(line[2])])

            id_map[line[1]] = i
            id_map_int[int(line[1])] = i
            id_map_inv[i] = line[1]
            id_map_inv_int[i] = int(line[1])
            ppi_graph.nodes[i]['id'] = i
            
            #print(i, id_map_int[int(line[2])])
            i+=1

        else:
            ppi_graph.add_edge(id_map_int[int(line[1])],id_map_int[int(line[2])])


# 0 : training = train_removed false : test_removed true
# 1 : test     = train_removed true  : test_removed false
# 2 : validation = true true


print("Graph info...")
print("Number of nodes: ", ppi_graph.number_of_nodes())
print("Number of connected components", nx.number_connected_components(ppi_graph))
print("Number of edges: ", ppi_graph.number_of_edges())
print()

with open("hs_ppi_graph.txt", "w+") as f:
    for e in ppi_graph.edges():
        a,b = e
        f.write(str(id_map_inv_int[a]) + " " + str(id_map_inv_int[b]) + "\n")

population = [0, 1, 2]
weights    = [0.8, 0.1, 0.1]
distribution_samples = choices(population, weights, k=ppi_graph.number_of_nodes())
print("Number of instances in training (0), test (1) and validation (2)\n",Counter(distribution_samples),sep='\n')
print("Number of instances in training (0), test (1) and validation (2)\n",Counter(distribution_samples),sep='\n', file=open("distribution_samples.txt", "w+"))
for i in range(ppi_graph.number_of_nodes()):
    if distribution_samples[i] == 0:
        ppi_graph.nodes[i]['test'] = False 
        ppi_graph.nodes[i]['val']  = False 
    elif distribution_samples[i] == 1:
        ppi_graph.nodes[i]['test'] = True
        ppi_graph.nodes[i]['val']  = False
    else:
        ppi_graph.nodes[i]['test'] = False
        ppi_graph.nodes[i]['val']  = True

    #print(i)
    #print(ppi_graph.nodes[id_map_inv[i]]['test'], ppi_graph.nodes[id_map_inv[i]]['val'], sep="\t", end="\n")


for component in list(nx.connected_components(ppi_graph)):
    if len(component) < 3:
        for node in component:
            ppi_graph.remove_node(node)


print("Checking the graph if smth is modified.")
print("Number of nodes: ", ppi_graph.number_of_nodes())
print("Number of connected components", nx.number_connected_components(ppi_graph))
print("Number of edges: ", ppi_graph.number_of_edges())

id_name_dict ={}
with open('BIOGRID-ORGANISM-Homo_sapiens-4.4.204.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        if line[1] == line[2]:
            continue
        id_name_dict[line[1]] = line[7]
        id_name_dict[line[2]] = line[8]

essential_dict = set()
with open('deg_hs_n-4.dat') as f:
    for line in f:
        essential_dict.add(line.strip())

class_map = {}
for i in id_map:
    my_key = id_map[i]
    my_str = id_name_dict[i]
    if my_str in essential_dict:
        class_map[my_key] = 1
    else:
        class_map[my_key] = 0

print("Number of essential genes", sum(class_map.values()))
print()

print("Creating class-map")
print('Creating id-map')
id_mappppp = {}
for i in range(ppi_graph.number_of_nodes()):
    id_mappppp[str(i)] = i

print("Writing graph to JSON file...")
json.dump(class_map, fp=open("hs_eppugnn-class_map.json", "w+"))
json.dump(json_graph.node_link_data(ppi_graph), fp=open("hs_eppugnn-G.json", "w+"))
json.dump({str(v): int(k) for k, v in id_map.items()}, fp=open("hs_eppugnn-id_map_inv.json", "w+"))
json.dump(id_mappppp, fp=open("hs_eppugnn-id_map.json", "w+"))
json.dump(id_map, fp=open("hs_eppugnn-id_map_dummy.json", "w+"))
