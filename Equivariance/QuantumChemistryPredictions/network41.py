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

def print(s_):
    s = str(s_)
    with open('outfile41.txt', 'a') as f:
            f.write(s+'\n')
            


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
        
#        print('Filter shape')
#        print(filters[0][0].shape)
        #Create parameter variables for each filter
        out = len(out_lst)
        mask = np.zeros((in_ch*nn,out))
        for i,tup in enumerate(out_lst):
            for el in tup:
                mask[el,i] = 1
        
        params1 = [[[]], [[], [], []], [[], [], [], [], []]]
        for l in range(L):
                for m in range(2*l+1):
                    params1[l][m].append(mask*tf.Variable(tf.truncated_normal((in_ch*nn, out), stddev=0.1)))

#        print('Parameter shape')
#        print(params1[0][0][0].shape)
        #Convolution with basis functions:
        basis_convolutions = map_on_nested(lambda t: tf.nn.conv3d(X_combination, t, strides=[1, 1, 1, 1, 1], 
                                                                  padding='SAME'), filters)

#        print('Basis convolutions')
#        print(basis_convolutions[0][0].shape)
        #Rotationally invariant filters
        products = []
        for l in range(L):
            for m in range(2*l+1):
                for m_ in range(2*l+1):
                    products.append(tf.square(matmul_im(basis_convolutions[l][m_], 
                                                        params1[l][m][0], in_ch*nn, out, width)))
            
        sums = sum(products)
#        print('Output')
#        print(sums.shape)
        #No mixing here
        return sums 


#X_channels: C H O N F

#Simplified

#layer1 = X
#print('Layer1')
layer1_out = [tuple(range(5))]*3
convoluted1 = rot_conv(X, 5, layer1_out, 'layer1', w)
layer2 = tf.nn.relu(convoluted1)




#Output is a dense layer of: layer1, layer2, layer3, layer4

layer1_out = tf.reduce_mean(X, axis=[-4, -3, -2]) #(batch, channels)
layer2_out = tf.reduce_mean(layer2, axis=[-4, -3, -2])

combined_layers_out = tf.concat([layer1_out,
                                 layer2_out], axis=-1)
                                

hidden = 128
mix_hidden = tf.Variable(tf.truncated_normal((5+3, hidden), stddev=0.5))
hidden_bias = tf.Variable(tf.truncated_normal([hidden],stddev=0.05))
hidden_layer = tf.nn.tanh(tf.matmul(combined_layers_out, mix_hidden)+hidden_bias)

mix_out = tf.Variable(tf.truncated_normal((hidden, 1), stddev=0.5))
mix_bias = tf.Variable(tf.truncated_normal([1],stddev=1))
y_ = 39.3597806534*tf.matmul(hidden_layer, mix_out)+mix_bias-405.230483484
                             



loss = tf.reduce_mean(tf.square(y_-y))
hartree = 627.5 #kcal/mol


lr = tf.placeholder(tf.float32,shape=[], name='lr')
train_step = tf.train.AdamOptimizer(lr).minimize(loss)

saver = tf.train.Saver()


config = tf.ConfigProto()
config.gpu_options.allow_growth = True

mini_batch = 20
epochs = 200

N = 100000

idx = np.arange(N)
np.random.seed(7)
np.random.shuffle(idx)
test_idx = idx[:int(0.1*N)]
train_idx = idx[int(0.1*N):]
current_lr = 0.1
with tf.Session(config = config) as sess:
    sess.run(tf.global_variables_initializer())
#    saver.restore(sess, './model41.ckpt')
    for e in range(epochs):
        saver.save(sess, './model41.ckpt')
        print('Epoch '+str(e))
        if e>15:
            current_lr = 1e-4
        np.random.shuffle(train_idx)
        with h5py.File('/home/wpl27/data.hdf5', 'r') as f:
            y_set = f['U0']
            X_set = f['image']
            losses = np.zeros(test_idx.size//mini_batch)
            for i in range(test_idx.size//mini_batch):
                batch_idx = list(np.sort(test_idx[i*mini_batch:(i+1)*mini_batch]))
                batch_X = X_set[batch_idx]
                batch_y = y_set[batch_idx]
                losses[i] = sess.run(loss, feed_dict={X: batch_X, y: batch_y, lr: current_lr})
            total_loss = np.sqrt(np.mean(losses))*hartree
            print('Loss: '+str(total_loss))
            training_loss = np.zeros(train_idx.size//mini_batch)
            for i in range(train_idx.size//mini_batch):
                batch_idx = list(np.sort(train_idx[i*mini_batch:(i+1)*mini_batch]))
                batch_X = X_set[batch_idx]
                batch_y = y_set[batch_idx]
                training_loss[i], _ = sess.run([loss,train_step], feed_dict={X: batch_X, y: batch_y, lr: current_lr})
            print('Training Loss: '+str(np.sqrt(np.mean(training_loss))*hartree))
            
