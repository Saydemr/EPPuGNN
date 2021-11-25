import sys
name = sys.argv[1]

id_name_dict ={}
with open('BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.203.tab3.txt') as f:
    f.readline()
    for line in f:
        line = line.strip().split('\t')
        if line[3] == line[4]:
            continue
        id_name_dict[line[3]] = line[7]
        id_name_dict[line[4]] = line[8]

essential_dict = set()
with open('deg_sc.dat') as f:
    for line in f:
        line = line.strip().split('\t')
        essential_dict.add(line[2])

with open (name) as emb:
    with open(name +'_out.csv','w+') as out:
        emb.readline()
        for line in emb:
            line = line.strip().split(' ')
            if id_name_dict[line[0]] in essential_dict:
                out.write('1\n')
            else:
                out.write('0\n')

with open(name) as emb:
    with open(name + '.csv') as out:
        emb.readline()
        for line in emb:
            line = line.strip().split(' ')
            out.write(','.join(line) + '\n')