for i in range(2006,2027):
    with open ('degannotation-e.dat', 'r') as f:
        with open ('deg_hs_' + str(i) + '.dat', 'w+') as g:
            f.readline()
            dataset = 'DEG' + str(i)
            for line in f:
                line = line.strip()
                line = line.split('\t')
                if line[7] == 'Homo sapiens' and line[0] == dataset:
                    g.write(line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3] + '\t' + line[4] + '\t' + line[5] + '\t' + line[6] + '\t' + line[7] + '\t' + line[8] + '\n')


gene_num_listed = {}

for i in range(2006,2027):
    with open ('deg_hs_' + str(i) + '.dat', 'r') as g:
        for line in g:
            line = line.strip()
            line = line.split('\t')
            if line[2] in gene_num_listed:
                gene_num_listed[line[2]] += 1
            else:
                gene_num_listed[line[2]] = 1

for i in range(1,18):
    with open ('deg_hs_n-' + str(i) + '.dat', 'w+') as g:
        for key in gene_num_listed:
            if gene_num_listed[key] >= i:
                g.write(key + '\n')
