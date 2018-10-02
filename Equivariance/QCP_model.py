#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np

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


I = 5 #number of atoms
w = 20 #width of image box
c = 8 #filter width
L = 3 #spherical harmonical L
nn = 6 #radial basis functions


#Radial basis:
#1, sin(r), cos(r) * exp(-r**2/2)
#Angular basis:
#1, x/r, y/r, z/r

wavelength = 1 #decay length in  Angstrom
image_width = 5 #molecule width in Angstrom
x = np.linspace(-image_width*c/w, image_width*c/w, c)

xx,yy,zz = np.meshgrid(x,x,x)
rr2 = xx**2+yy**2+zz**2
rr = np.sqrt(rr2)

radials = [np.exp(-rr), 
           np.exp(-rr/2)*rr, 
           np.exp(-rr/2)*(1-rr/2),
           np.exp(-rr/3)*rr2,
           np.exp(-rr/3)*rr*(1-rr/6),
           np.exp(-rr/3)*(1-2*rr/3+2*rr2*2/27)]


ortho = []

for arr in radials:
    new = np.copy(arr)
    for old in ortho:
        new -= old*np.sum(old*new)/np.sum(old**2)
    ortho.append(new)
                    
ortho = np.stack(ortho,axis=-1)
                    

SHs = [[np.ones(rr.shape)], 
       [xx/rr, yy/rr, zz/rr], 
       [xx*yy/rr2, yy*zz/rr2, zz*xx/rr2, (xx**2-yy**2)/rr2, (2*zz**2-xx**2-yy**2)/rr2]]





def rot_conv(X_combination, in_ch, out_lst):
    filters = [[0], [0, 0, 0], [0, 0, 0, 0, 0]]

    for l in range(L):
        for m in range(2*l+1):
            exp_SHs = np.expand_dims(SHs[l][m], axis=-1)
            filters[l][m] = diagonalize(normalize(ortho*exp_SHs), in_ch)


    filters = map_on_nested(lambda x: tf.convert_to_tensor(x, preferred_dtype=tf.float32), filters)

    #Create parameter variables for each filter
    out = len(out_lst)
    mask = np.zeros((in_ch*nn,out))
    for i,tup in enumerate(out_lst):
        for el in tup:
            mask[el,i] = 1

    init_params1 = [[[]], [[], [], []], [[], [], [], [], []]]
    np.random.seed(7)
    magnitude = 0.1 
    for l in range(L):
            for m in range(2*l+1):
                init_params1[l][m].append(2*magnitude*np.random.rand(in_ch*nn*out).reshape(in_ch*nn, out).astype('float32')-magnitude)


    params1 = [[[]], [[], [], []], [[], [], [], [], []]]
    for l in range(L):
            for m in range(2*l+1):
                with tf.variable_scope(str(l)+'_'+str(m)):
                    ws = tf.get_variable('weights', initializer=init_params1[l][m][0])
                    params1[l][m].append(ws)
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
                                                    params1[l][m][0], in_ch*nn, out, w)))

    sums = sum(products)
    convolved = tf.identity(sums, name='convolved')
    return convolved


def inference(X):
    activations = []
    with tf.variable_scope('layer1'):
        tuple_out = [tuple(range(5))]*3
        channels_in = I
        convolved = rot_conv(X, channels_in, tuple_out)
        activated = tf.nn.relu(convolved, name='activated')
        activations.append(activated)
        tf.summary.histogram('Activation',activated)

    X_mean = tf.reduce_mean(X, axis=[-4, -3, -2]) #(batch, channels)

    layers = []
    for t in activations:
        layers.append(tf.reduce_mean(t,axis=[-4,-3,-2]))

#    combined_layers_out = tf.concat(layers+[X_mean], axis=-1, name='concat')
    combined_layers_out = X_mean
        
    with tf.variable_scope('hidden') as scope:
        hidden = 128
        weights = tf.get_variable(name='weights',initializer=tf.truncated_normal((5, hidden), stddev=0.5))
        bias = tf.get_variable(name='bias', initializer=tf.truncated_normal([hidden], stddev=0.05))
        activated = tf.nn.tanh(tf.matmul(combined_layers_out, weights)+bias, name=scope.name)
    with tf.variable_scope('out') as scope:
        weights = tf.get_variable(name='weights',initializer=tf.truncated_normal((hidden, 1), stddev=0.5))
        bias = tf.get_variable(name='bias', initializer=tf.truncated_normal([1], stddev=1))
        y_ = 39.3597806534*tf.matmul(activated,weights)+bias-405.230483484
        
    return y_
