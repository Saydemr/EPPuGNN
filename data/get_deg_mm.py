with open ('degannotation-e.dat', 'r') as f:
    with open ('deg_mm.dat', 'w+') as g:
        f.readline()
        for line in f:
            line = line.strip()
            line = line.split('\t')
            if line[7] == 'Mus musculus' and line[0] == 'DEG2005':
                g.write(line[0] + '\t' + line[1] + '\t' + line[2] + '\t' + line[3] + '\t' + line[4] + '\t' + line[5] + '\t' + line[6] + '\t' + line[7] + '\t' + line[8] + '\n')
