import tensorflow as tf
import numpy as np
from equivariant_convolution import conv

def inference(X):
    activations = []
    with tf.variable_scope('layer1'):
        tuple_out = [tuple(range(5))]*3
        channels_in = I
        convolved = conv(X, channels_in, tuple_out)
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
