import numpy as np
import h5py

total_molecules = 100000
U0s = np.zeros(total_molecules)

for m in range(total_molecules):
    print(m)
    fname = '/home/wpl27/Data/Data/dsgdb9nsd_%06d.xyz' % (m+1)
    with open(fname) as f:
        for n,line in enumerate(f):
            words = line.split()
            if n==1:
                U0s[m] = words[12]
        
print('Mean: ', np.mean(U0s))
print('STD: ', np.std(U0s))

U0s = (U0s-np.mean(U0s))/np.std(U0s)

#with h5py.File('data.hdf5', 'r+') as f:
#    U0 = f['U0']
#    U0[:] = U0s.reshape((-1, 1))
    
