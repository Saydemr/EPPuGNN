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
        line = line.strip().split('\t')
        essential_dict.add(line[0])


class_map = {}
with open ('ppiemb.txt') as emb:
    with open('ppiemb_essentiality.txt','w+') as out:
        emb.readline()
        for line in emb:
            line = line.strip().split(' ')
            if id_name_dict[line[0]] in essential_dict:
                out.write('1\n')
            else:
                out.write('0\n')