#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
import h5py


def map_on_nested(func, lst):
    if type(lst)!=list:
        return func(lst)
    return list(map(lambda x: map_on_nested(func, x), lst))


def normalize(flter):
    integral = np.sum(flter**2)
    return flter/np.sqrt(integral)

def matmul_im(im, f, in_channels, out_channels, width):
    im_ = tf.reshape(im, (-1, in_channels))
    return tf.reshape(tf.matmul(im_, f), (-1, width, width, width, out_channels))




I = 4 #number of atoms
w = 32 #width of image box





#Define filters:

c = 16 #filter width
L = 3 #spherical harmonical L
nn = 6 #radial basis functions


#Radial basis:
#1, sin(r), cos(r) * exp(-r**2/2)
#Angular basis:
#1, x/r, y/r, z/r

wavelength = 1 #decay length in  Angstrom
image_width = 6.5 #molecule width in Angstrom
x = np.linspace(-2.5,2.5, c)

xx,yy,zz = np.meshgrid(x,x,x)
rr2 = xx**2+yy**2+zz**2
rr = np.sqrt(rr2)

radials = [np.exp(-rr), 
          np.exp(-1.5*rr), 
          np.exp(-2*rr),
          np.exp(-2.5*rr),
          np.exp(-3*rr),
          np.exp(-3.5*rr)]

ortho = []

for arr in radials:
    new = np.copy(arr)
    for old in ortho:
        new -= old*np.sum(new*old)/np.sum(old**2)
    ortho.append(new)
                    
                    
radials = np.stack(radials,axis=-1)
ortho = np.stack(ortho,axis=-1)                    

SHs = [[np.ones(rr.shape)], 
       [xx/rr, yy/rr, zz/rr], 
       [xx*yy/rr2, yy*zz/rr2, zz*xx/rr2, (xx**2-yy**2)/rr2, (2*zz**2-xx**2-yy**2)/rr2]]



def reduce_filter(flter):
    a,b,c,d,e = flter.shape
    return flter.reshape((a//2,2,b//2,2,c//2,2,d,e)).mean(axis=(1,3,5))



def diagonalize(arr, in_ch):
    new = np.zeros((c, c, c, in_ch, nn*in_ch))
    for i in range(in_ch):
        new[:, :, :, i, i:(i+nn)] = arr
    return new

#Begin tensorflow
X = tf.placeholder(tf.float32, shape=[None, w, w, w, I], name='X')

def rot_conv(X_combination, in_ch, out_lst,  name, width):
    with tf.name_scope(name) as scope:
        filters = [[0], [0, 0, 0], [0, 0, 0, 0, 0]]

        for l in range(L):
            for m in range(2*l+1):
                exp_SHs = np.expand_dims(SHs[l][m], axis=-1)
                filters[l][m] = diagonalize(normalize(ortho*exp_SHs), in_ch)


        for i in range(int(np.log2(w/width))):
            filters = map_on_nested(reduce_filter, filters)        
        
        filters = map_on_nested(lambda x: tf.convert_to_tensor(x, preferred_dtype=tf.float32), filters)
        
        #Create parameter variables for each filter
        out = len(out_lst)
        mask = np.zeros((in_ch*nn,out))
        for i,tup in enumerate(out_lst):
            for el in tup:
                mask[el,i] = 1
        
        
        initial_params = [[[]], [[], [], []], [[], [], [], [], []]]
        for l in range(L):
            for m in range(2*l+1):
                initial_params[l][m].append(2*np.random.rand(in_ch*nn*out).reshape((in_ch*nn,out)).astype('float32')-1)
        
        
        
        params1 = [[[]], [[], [], []], [[], [], [], [], []]]
        for l in range(L):
                for m in range(2*l+1):
                    params1[l][m].append(mask*tf.Variable(initial_params[l][m][0], name=str(l)+'_'+str(m)))
#                    params1[l][m].append(mask*tf.Variable(tf.truncated_normal((in_ch*nn, out), stddev=1), name=str(l)+'_'+str(m)))

        #Convolution with basis functions:
        basis_convolutions = map_on_nested(lambda t: tf.nn.conv3d(X_combination, t, strides=[1, 1, 1, 1, 1], 
                                                                  padding='SAME'), filters)

        #Rotationally invariant filters
        products = []
        for l in range(L):
            for m in range(2*l+1):
                for m_ in range(2*l+1):
                    products.append(tf.square(matmul_im(basis_convolutions[l][m_], 
                                                        params1[l][m][0], in_ch*nn, out, width)))
            
        equivariant = sum(products)

        products2 = []
        for l in range(L):
            for m in range(2*l+1):
                products2.append(matmul_im(basis_convolutions[l][m], params1[l][m][0], in_ch*nn, out, width))
        norm_conv = sum(products2)
        
        return equivariant, norm_conv 


#X_channels: C H O N F


equivariant_1_, normal_1_ = rot_conv(X, 4, [tuple(range(4))], 'a', w)
equivariant, normal = tf.nn.relu(equivariant_1_), tf.nn.relu(normal_1_)




with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    with h5py.File('rotated_molecule.hdf5', 'r') as f:
        X_set = f['image']
        y1, y2, variables = sess.run([equivariant, normal, tf.trainable_variables()], feed_dict={X: X_set[:10]})
        summed1 = y1.sum(axis=(1,2,3))
        summed2 = y2.sum(axis=(1,2,3))
        print('Equivariant:')
        print(summed1)   
        print(np.std(summed1,axis=0)/np.mean(summed1,axis=0))
        print('Normal:')
        print(summed2)   
        print(np.std(summed2,axis=0)/np.mean(summed2,axis=0))
        print('Variables:')
        print(tf.trainable_variables())
