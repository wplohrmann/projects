import numpy as np
import pandas as pd
import pickle
import h5py
import pdb

def to_float(s):
    if 'e' not in s:
        return float(s)
    else:
        return 0

def xyzToHDF5(N_start, N, filename, total_molecules):
    df = pd.DataFrame(columns=['id', 'element', 'x', 'y', 'z', 'U0'])

    for m in range(N_start, N_start + N):
        fname = './Data/dsgdb9nsd_%06d.xyz' % (m+1)
        with open(fname) as f:
            for n,line in enumerate(f):
                words = line.split()
                if n==0:
                    na = int(line)
                if n==1:
                    i_d = words[1]
                    U0 = words[12]
                if n>1 and n<=na:
                    df = df.append({'id' : i_d, 'element' : words[0], 
                                    'x' : words[1], 'y' : words[2], 'z': words[3],
                                    'U0' : U0}, ignore_index=True)
        


    df['x'] = df['x'].apply(to_float)
    df['y'] = df['y'].apply(to_float)
    df['z'] = df['z'].apply(to_float)

    df['id'] = df['id'].apply(pd.to_numeric)

    positions = np.array(df.iloc[:,2:5])
    ids = np.array(df['id'])
    elements = np.array(df['element'])
    duplicate_U0s = np.array(df['U0'])

    for i in range(np.max(ids)):
        molecule_positions = positions[ids==i+1]

        #Center the molecule at the origin, so it fits in the smallest possible cube
        positions[ids==i+1] -= (np.max(molecule_positions, axis=0) +
                                np.min(molecule_positions, axis=0))/2


    #Specifying the input
    #20x20x20 grid
    biggest = 10
    grid_size = biggest*1.2 # Side length in Å of box
    grid_points = 20 # 20x20x20 boxes
    atoms = 5 # CHONF

    x = np.linspace(-grid_size,grid_size, grid_points)

    xx,yy,zz = np.meshgrid(x, x, x)

    radii = np.array([0.75, 0.31, 0.66, 0.71, 0.57]) #covalent radii of elements
    elements_dict = {'C': 0, 'H': 1, 'O': 2, 'N': 3, 'F': 4} 
    molecule_fields = np.zeros((N,grid_points, grid_points, grid_points, atoms))

    normalizations = 1/np.sqrt(2*np.pi*radii**2)


    for n in np.arange(N):
        molecule_coords = positions[ids==1+n]
        image = np.zeros((grid_points,grid_points,grid_points, atoms))
        for k in np.arange(molecule_coords.shape[0]):
            x_pos,y_pos,z_pos = molecule_coords[k,0], molecule_coords[k,1], molecule_coords[k,2] 
            element = elements_dict[elements[k]]
            normalization = normalizations[element]
            
            radius = radii[element]
            addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
            
            image[:, :, :, element] += addition
        
        molecule_fields[n] = image


    sorted_U0s, indices = np.unique(duplicate_U0s, return_index=True)
    assert(sorted_U0s.size == N)

    U0s = np.array([duplicate_U0s[l] for l in indices], dtype=np.dtype('f')).reshape((-1, 1))

    g = h5py.File(filename, 'a')
    dset = g.require_dataset('molecule_fields', (total_molecules, 20, 20, 20, 5), dtype=np.dtype("f"))
    dset2 = g.require_dataset('U0',  (total_molecules, 1), dtype=np.dtype('f'))
                    
                    
    dset[N_start:N_start+N] = molecule_fields
    dset2[N_start:N_start+N] = U0s

    g.close()

xyzToHDF5(0, 10, "data.hdf5", 102)

