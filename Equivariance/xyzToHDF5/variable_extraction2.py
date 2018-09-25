#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
import h5py
import pickle

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



I = 5 #number of atoms
w = 20 #width of image box





#Define filters:

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

radials =          [np.exp(-rr), 
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
y = tf.placeholder(tf.float32, shape=[None, 1], name='y_input')


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
        
        print('Filter shape')
        print(filters[0][0].shape)
        #Create parameter variables for each filter
        out = len(out_lst)
        mask = np.zeros((in_ch*nn,out))
        for i,tup in enumerate(out_lst):
            for el in tup:
                mask[el,i] = 1
        
        init_params1 = [[[]], [[], [], []], [[], [], [], [], []]]
        np.random.seed(7)
        for l in range(L):
                for m in range(2*l+1):
                    init_params1[l][m].append(0.02*np.random.rand(in_ch*nn*out).reshape(in_ch*nn, out).astype('float32')-0.01)


        params1 = [[[]], [[], [], []], [[], [], [], [], []]]
        for l in range(L):
                for m in range(2*l+1):
                    params1[l][m].append(mask*tf.Variable(init_params1[l][m][0], trainable=True))

        print('Parameter shape')
        print(params1[0][0][0].shape)
        #Convolution with basis functions:
        basis_convolutions = map_on_nested(lambda t: tf.nn.conv3d(X_combination, t, strides=[1, 1, 1, 1, 1], 
                                                                  padding='SAME'), filters)

        print('Basis convolutions')
        print(basis_convolutions[0][0].shape)
        #Rotationally invariant filters
        products = []
        for l in range(L):
            for m in range(2*l+1):
                for m_ in range(2*l+1):
                    products.append(tf.square(matmul_im(basis_convolutions[l][m_], 
                                                        params1[l][m][0], in_ch*nn, out, width)))
            
        sums = sum(products)
        print('Output')
        print(sums.shape)
        #No mixing here
        return sums 


#X_channels: C H O N F

#Simplified

#layer1 = X
print('Layer1')
layer1_out = [tuple(range(5))]*256
convoluted1 = rot_conv(X, 5, layer1_out, 'layer1', w)
layer2 = tf.nn.tanh(convoluted1)
print('Layer2')
layer2_out = [tuple(range(16))]*256
layer2_slice = layer2[:,:,:,:,:16]
convoluted2 = rot_conv(layer2_slice, 16, layer2_out, 'layer2', w)
layer3 = tf.nn.tanh(convoluted2)

print('Layer3')
layer3_out = [tuple(range(16))]*256
layer3_slice = layer2[:,:,:,:,:16]
convoluted3 = rot_conv(layer3_slice, 16, layer3_out, 'layer3', w)
layer4 = tf.nn.tanh(convoluted3)




#Output is a dense layer of: layer1, layer2, layer3, layer4

layer1_out = tf.reduce_mean(X, axis=[-4, -3, -2]) #(batch, channels)
layer2_out = tf.reduce_mean(layer2, axis=[-4, -3, -2])
layer3_out = tf.reduce_mean(layer3, axis=[-4, -3, -2])
layer4_out = tf.reduce_mean(layer4, axis=[-4, -3, -2])

combined_layers_out = tf.concat([layer1_out,
                                 layer2_out,
                                 layer3_out,
                                 layer4_out], axis=-1)
                                

hidden = 256
mix_hidden = tf.Variable(tf.truncated_normal((5+256*3, hidden), stddev=0.5))
hidden_layer = tf.nn.tanh(tf.matmul(combined_layers_out, mix_hidden))

mix_out = tf.Variable(tf.truncated_normal((hidden, 1), stddev=0.5))
y_ = tf.matmul(hidden_layer, mix_out)
                             



loss = tf.reduce_mean(tf.square(y_-y))
hartree = 627.5 #kcal/mol


lr = tf.placeholder(tf.float32,shape=[], name='lr')
train_step = tf.train.AdamOptimizer(lr).minimize(loss)

saver = tf.train.Saver()

saver_b = tf.train.Saver([v for v in tf.all_variables() if not ('Adam' in v.name and 'layer' in v.name)])

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

mini_batch = 10
epochs = 200

N = 100000

idx = np.arange(N)
np.random.shuffle(idx)
test_idx = idx[:int(0.1*N)]
train_idx = idx[int(0.1*N):]
current_lr = 5e-4
with tf.Session(config = config) as sess:
    saver.restore(sess,'./model46.ckpt')
    the_vars = sess.run(tf.global_variables())

    filter_params = [[[]], [[], [], []], [[], [], [], [], []]]
    print('Length: ', len(the_vars))
    i = 0
    for l in range(L):
        for m in range(2*l+1):
            filter_params[l][m].append(the_vars[i])
            i += 1
    print(i)
    with open('params46.pckl', 'wb') as f:
        pickle.dump(filter_params, f)



        
            

