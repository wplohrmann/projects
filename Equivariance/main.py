import tensorflow as tf
import glob

filenames = glob.glob("TFRecords/*")

def parser(filename_queue):
    reader = tf.TFRecordReader()

    _, serialized_example = reader.read(filename_queue)

    features = tf.parse_single_example(
            serialized_example,
            features={
                'molecule_fields_raw': tf.FixedLenFeature([], tf.string),
                'U0s_raw': tf.FixedLenFeature([], tf.string)})
    X_1d = tf.decode_raw(features['molecule_fields_raw'], tf.float32)
    y_1d = tf.decode_raw(features['U0s_raw'], tf.float32)

    X = tf.reshape(X_1d, (-1, 20, 20, 20, 5))
    y = tf.reshape(y_1d, (-1, 1))
    
    return X, y
