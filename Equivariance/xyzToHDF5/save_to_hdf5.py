import pickle
import numpy as np
import h5py

total_molecules = 100000

g = h5py.File('data.hdf5', 'w')
dset = g.create_dataset('image', (total_molecules, 20, 20, 20, 5))
dset2 = g.create_dataset('U0',  (total_molecules, 1))
                    
                    
for n in range(total_molecules//100):
    begin_index=n*100
    with open('./Compiled/data'+str(begin_index)+'.pckl', 'rb') as f:
            set = pickle.load(f)
            X = set[:, 1:].reshape((100, 20, 20, 20, 5))  
            y = set[:, 0].reshape((-1, 1))          
            dset[begin_index:begin_index+100] = X
            dset2[begin_index:begin_index+100] = y
    print(n)
g.close()

