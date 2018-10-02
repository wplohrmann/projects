import tensorflow as tf
import glob
from QCP_model import inference

filenames = glob.glob("TFRecords/*")
def input_fn():
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

        return next_element

def model_fn(features, labels, mode, params):
    net = tf.feature_column.input_layer(features, params['feature_columns'])
    y_ = inference(net)
    if mode == tf.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode, y_)

    loss = tf.reduce_mean(tf.square(y_-y), name='loss')
    hartree = 627.5 #kcal/mol
    rme = tf.sqrt(loss)*hartree
    tf.summary.scalar('RME', rme)

    if mode == tf.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=loss)

    if mode == tf.ModeKeys.TRAIN:
        optimizer = tf.train.AdamOptimizer(params['lr'])
        train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)


