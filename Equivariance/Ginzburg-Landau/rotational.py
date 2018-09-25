#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
import pdb
from scipy.special import sph_harm
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

def diagonalize(arr, in_ch):
    new = np.zeros((c, c, c, in_ch, nn*in_ch))
    for i in range(in_ch):
        new[:, :, :, i, i:(i+nn)] = arr
    return new

def empty(L):
    lst = []
    for l in range(L):
        lst.append([])
        for m in range(2*l+1):
            lst[l].append(0)
    return lst


w = 20 #width of image box
c = 8 #filter width


L = 5 #spherical harmonical L
nn = c//2 #radial basis functions

#Degrees of freedom in 8x8x8 is 8**3
#nn * L**2 = 8**3 => L~11

x = np.linspace(-1,1,c)
xx,yy,zz = np.meshgrid(x,x,x)

rr2 = xx**2+yy**2+zz**2
rr = np.sqrt(rr2)

tmp = np.maximum(np.abs(xx),np.abs(yy))

shells = np.maximum(tmp,np.abs(zz))
shells = np.round(shells*100)

radials = [(shells==i)*1 for i in np.unique(shells)]

ortho = np.stack(radials,axis=-1)
                    
def real_SH(l,m,theta,phi):
    added = sph_harm(m,l,theta,phi)+np.sign(m)*sph_harm(-m,l,theta,phi)
    return np.absolute(added)

phi = np.arctan(zz/rr)
theta = np.arctan2(yy,xx)


SHs = empty(L)
for l in range(L):
    for m in range(2*l+1):
        m_ = m-l
        SHs[l][m] = real_SH(l,m_,theta,phi)


def conv(X_combination, in_ch, out):
    filters = empty(L)
    for l in range(L):
        for m in range(2*l+1):
            exp_SHs = np.expand_dims(SHs[l][m], axis=-1)
            filters[l][m] = diagonalize(normalize(ortho*exp_SHs), in_ch)


    filters = map_on_nested(lambda x: tf.convert_to_tensor(x, preferred_dtype=tf.float32), filters)



    magnitude = 1

    params1 = empty(L)
    for l in range(L):
            for m in range(2*l+1):
                with tf.variable_scope(str(l)+'_'+str(m)):
                    ws = tf.get_variable('weights', initializer=tf.truncated_normal([in_ch*nn, out], stddev=magnitude))
                    params1[l][m] = ws
                    tf.summary.histogram('weights', ws)


 
    #Convolution with basis functions:
    basis_convolutions = map_on_nested(lambda t: tf.nn.conv3d(X_combination, t, strides=[1, 1, 1, 1, 1], 
                                                              padding='SAME'), filters)


    #Rotationally invariant filters
    products = []
    for l in range(L):
        for m in range(2*l+1):
            for m_ in range(2*l+1):
                products.append(tf.square(matmul_im(basis_convolutions[l][m_], 
                                                    params1[l][m], in_ch*nn, out, w)))

    sums = sum(products)
    convolved = tf.identity(sums, name='convolved')
    return convolved



