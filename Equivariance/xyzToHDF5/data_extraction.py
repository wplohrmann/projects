#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3
import numpy as np
import pandas as pd
import pickle


N = 10000
df = pd.DataFrame(columns=['id', 'atom', 'x', 'y', 'z', 'U0'])

for m in range(N):
    fname = '/home/wpl27/Data/Data/dsgdb9nsd_%06d.xyz' % (m+1)
    with open(fname) as f:
        for n,line in enumerate(f):
            words = line.split()
            if n==0:
                na = int(line)
            if n==1:
                i_d = words[1]
                U0 = words[12]
            if n>1 and n<=na:
                df = df.append({'id' : i_d, 'atom' : words[0], 
                                'x' : words[1], 'y' : words[2], 'z': words[3],
                                'U0' : U0}, ignore_index=True)
        

def remove_scientific(s):
    try:
        float(s)
        return s
    except:
        return '0'

df['x'] = df['x'].apply(remove_scientific)
df['y'] = df['y'].apply(remove_scientific)
df['z'] = df['z'].apply(remove_scientific)

df['x'] = df['x'].apply(pd.to_numeric)
df['y'] = df['y'].apply(pd.to_numeric)
df['z'] = df['z'].apply(pd.to_numeric)
df['id'] = df['id'].apply(pd.to_numeric)

positions = np.array(df.iloc[:,2:5])
ids = np.array(df['id'])

print(np.max(np.abs(positions)))

for i in range(np.max(ids)):
    pos = positions[ids==i+1]
    biggest = np.max(pos, axis=0)
    smallest = np.min(pos, axis=0)
    positions[ids==i+1] -= (biggest+smallest)/2

biggest = np.max(np.abs(positions))
print(biggest)

#Specifying the input
#20x20x20 grid
grid_size = biggest*1.2 # Side length in Å of box
grid_resolution = 20 # 20x20x20 boxes
atoms = 5 # CHONF

x = np.linspace(-grid_size,grid_size, grid_resolution)





xx,yy,zz = np.meshgrid(x, x, x)

radii = np.array([0.75, 0.31, 0.66, 0.71, 0.57])
atom_types = {'C': 0, 'H': 1, 'O': 2, 'N': 3, 'F': 4} 
molecules = np.zeros((N,grid_resolution*grid_resolution*grid_resolution*atoms))



for n in np.arange(N):
    molecule = df[df['id']==(n+1)]
    image = np.zeros((grid_resolution,grid_resolution,grid_resolution, atoms))
    for k in np.arange(len(molecule)):
        a = atom_types[molecule.iloc[k,1]]
        x_pos,y_pos,z_pos = molecule.iloc[0,2:5]
        radius = radii[a]
        normalization = 1/np.sqrt(2*np.pi*radius**2)
        addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
        image[:, :, :, a] += addition
        
    molecules[n] = image.flatten()


U0s = np.zeros((N,1))
for n in np.arange(N):
    molecule = df[df['id']==(n+1)]
    U0s[n] = float(molecule.iloc[0,5])


data = np.hstack((U0s,molecules))

for i in range(N//100):
    with open('./Compiled/data'+str(i)+'.pckl', 'wb') as f:
        pickle.dump(data[100*i:100*(i+1)], f)

