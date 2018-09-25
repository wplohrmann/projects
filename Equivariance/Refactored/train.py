#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
import h5py
import model



I = 5 #number of atoms
w = 20 #width of image box



#Begin tensorflow
X = tf.placeholder(tf.float32, shape=[None, w, w, w, I], name='X')
y = tf.placeholder(tf.float32, shape=[None, 1], name='y_input')

y_ = model.inference(X)

loss = tf.reduce_mean(tf.square(y_-y), name='loss')
hartree = 627.5 #kcal/mol
rme = tf.sqrt(loss)*hartree
tf.summary.scalar('RME', rme)

lr = tf.placeholder(tf.float32,shape=[], name='lr')

#Old:
#train_step = tf.train.AdamOptimizer(lr).minimize(loss)

#New:
## Optimizer definition - nothing different from any classical example
opt = tf.train.AdamOptimizer(lr)

## Retrieve all trainable variables you defined in your graph
tvs = tf.trainable_variables()
## Creation of a list of variables with the same shape as the trainable ones
# initialized with 0s
accum_vars = [tf.Variable(tf.zeros_like(tv.initialized_value()), trainable=False) for tv in tvs]
zero_ops = [tv.assign(tf.zeros_like(tv)) for tv in accum_vars]

## Calls the compute_gradients function of the optimizer to obtain... the list of gradients
gvs = opt.compute_gradients(loss, tvs)

## Adds to each element from the list you initialized earlier with zeros its gradient (works because accum_vars and gvs are in the same order)
accum_ops = [accum_vars[i].assign_add(gv[0]) for i, gv in enumerate(gvs)]

## Define the training step (part with variable value update)
train_step = opt.apply_gradients([(accum_vars[i], gv[1]) for i, gv in enumerate(gvs)])

#END New

#saver = tf.train.Saver()

writer = tf.summary.FileWriter('./summaries')
writer.add_graph(tf.get_default_graph())
merged_summary = tf.summary.merge_all()
saver=tf.train.Saver()





mini_batch = 20
num_batch = 2
epochs = 200

N = 100000

idx = np.arange(N)
np.random.shuffle(idx)
test_idx = idx[:int(0.1*N)]
train_idx = idx[int(0.1*N):]
current_lr = 5e-3


with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())
#    saver.restore(sess, './saved/m1.ckpt')
    sess.run(zero_ops)
    for e in range(epochs):
        saver.save(sess, './saved/m1.ckpt')
        if e>15:
            current_lr = 5e-4
        np.random.shuffle(train_idx)
        with h5py.File('/home/wpl27/data.hdf5', 'r') as f:
            y_set = f['U0']
            X_set = f['image']
            for i in range(train_idx.size//mini_batch):
                batch_idx = list(np.sort(train_idx[i*mini_batch:(i+1)*mini_batch]))
                batch_X = X_set[batch_idx]
                batch_y = y_set[batch_idx]
                if i % 10 ==0:
                    s= sess.run(merged_summary, feed_dict={X: batch_X, y: batch_y, lr: current_lr})
                    writer.add_summary(s,i+e*train_idx.size//mini_batch)

                sess.run(accum_ops, feed_dict={X: batch_X, y: batch_y})

                if i % num_batch == num_batch-1:
                    sess.run(train_step, feed_dict={lr: current_lr})
                    sess.run(zero_ops)
