#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3

import tensorflow as tf
import numpy as np
from rotational import conv
import pdb




def inference(X):
    activations = []
    with tf.variable_scope('layer1'):
        out = 10
        in_ch = 1
        convolved = conv(X, in_ch, out)
        tf.summary.histogram('Convolved',convolved)
            


    reduced = tf.reduce_mean(convolved,axis=[-4,-3,-2])
    tf.summary.histogram('Reduced', reduced)


    with tf.variable_scope('out') as scope:
        weights = tf.get_variable(name='weights',initializer=tf.truncated_normal([out, 1], stddev=0.5))
        bias = tf.get_variable(name='bias', shape = [1], initializer=tf.zeros_initializer())
        y = tf.matmul(reduced,weights)+bias


    return y*5e-5
