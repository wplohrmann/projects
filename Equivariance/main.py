import tensorflow as tf
import glob

filenames = glob.glob("TFRecords/*")

def parser(example_proto):
    features = tf.parse_single_example(
            example_proto,
            features={
                'molecule_fields_raw': tf.FixedLenFeature([], tf.string),
                'U0s_raw': tf.FixedLenFeature([], tf.string)})
    X_1d = tf.decode_raw(features['molecule_fields_raw'], tf.float32)
    y_1d = tf.decode_raw(features['U0s_raw'], tf.float32)

    X = tf.reshape(X_1d, (-1, 20, 20, 20, 5))
    y = tf.reshape(y_1d, (-1, 1))
    

    return X, y

dataset = tf.data.TFRecordDataset(filenames[0])
dataset = dataset.map(parser)

iterator = dataset.make_one_shot_iterator()

next_element = iterator.get_next()


with tf.Session() as sess:
    arrs = sess.run(next_element)
    for arr in arrs:
        print(arr.shape)
