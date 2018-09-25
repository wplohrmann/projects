#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3


N = 100000


biggest = 10
#Specifying the input
#20x20x20 grid
grid_size = biggest*1.2 # Side length in Å of box
grid_resolution = 20 # 20x20x20 boxes
atoms = 5 # CHONF

biggest = 0
for m in range(N):
    if m % 100 == 0:
        print(m)
    fname = '/home/wpl27/Data/Data/dsgdb9nsd_%06d.xyz' % (m+1)
    with open(fname) as f:
        x_list = []
        y_list = []
        z_list = []
        for n,line in enumerate(f):
            words = line.split()
            if n==0:
                na = int(line)
            if n>1 and n<=na:
                try:
                    x_list.append(float(words[1]))
                    y_list.append(float(words[2]))
                    z_list.append(float(words[3]))
                except:
                    pass
        if (max(y_list)-min(y_list))>biggest:
            biggest = max(y_list)-min(y_list)       
        if (max(x_list)-min(x_list))>biggest:
            biggest = max(x_list)-min(x_list)       
        if (max(z_list)-min(z_list))>biggest:
            biggest = max(z_list)-min(z_list)       
print(biggest)
