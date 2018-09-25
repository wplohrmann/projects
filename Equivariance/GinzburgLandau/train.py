#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
import h5py
from model import inference



I = 1 #number of input channels
w = 20 #width of image box



#Begin tensorflow
X = tf.placeholder(tf.float32, shape=[None, w, w, w, I], name='X')
y = tf.placeholder(tf.float32, shape=[None, 1], name='y_input')

y_ = 1224009+287328*inference(X)

loss = tf.reduce_mean(tf.square(y_-y), name='loss')
rme = tf.sqrt(loss)
tf.summary.scalar('RME', rme)

lr = 2e-4

#Old:
train_step = tf.train.AdamOptimizer(lr).minimize(loss)

#New:
## Optimizer definition - nothing different from any classical example
#opt = tf.train.AdamOptimizer(lr)

## Retrieve all trainable variables you defined in your graph
#tvs = tf.trainable_variables()
## Creation of a list of variables with the same shape as the trainable ones
# initialized with 0s
#accum_vars = [tf.Variable(tf.zeros_like(tv.initialized_value()), trainable=False) for tv in tvs]
#zero_ops = [tv.assign(tf.zeros_like(tv)) for tv in accum_vars]

## Calls the compute_gradients function of the optimizer to obtain... the list of gradients
#gvs = opt.compute_gradients(loss, tvs)

## Adds to each element from the list you initialized earlier with zeros its gradient (works because accum_vars and gvs are in the same order)
#accum_ops = [accum_vars[i].assign_add(gv[0]) for i, gv in enumerate(gvs)]

## Define the training step (part with variable value update)
#train_step = opt.apply_gradients([(accum_vars[i], gv[1]) for i, gv in enumerate(gvs)])

#END New

saver = tf.train.Saver()

writer = tf.summary.FileWriter('./summaries/L5_fm10_relu_lr2e4_batch5_mag5e4')
writer.add_graph(tf.get_default_graph())
merged_summary = tf.summary.merge_all()





mini_batch = 5
num_batch = 1

N = 100
epochs = 2000000//N


y_set = np.loadtxt('train_y.csv',delimiter=',')
X_set = np.loadtxt('train_X.csv',delimiter=',')
idx = np.arange(N)


with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())
#    saver.restore(sess, './saved/m1.ckpt')
#    sess.run(zero_ops)
    for e in range(epochs):
#        saver.save(sess, './saved/m1.ckpt')
        np.random.shuffle(idx)
        y_set = y_set[idx]
        X_set = X_set[idx]
        
        for i in range(N//mini_batch):
            batch_X = X_set[mini_batch*i:mini_batch*(i+1)]
            batch_y = y_set[mini_batch*i:mini_batch*(i+1)] 
            batch_X = batch_X.reshape((-1, 20, 20, 20, 1))
            batch_y = batch_y.reshape((-1, 1))
            s = sess.run(merged_summary, feed_dict={X: batch_X, y: batch_y})
               
            writer.add_summary(s,i+e*idx.size//mini_batch)
               
            sess.run(train_step, feed_dict={X: batch_X, y: batch_y})
 
