import tensorflow as tf
import glob
from QCP_model import inference

filenames = glob.glob("TFRecords/*")
def input_fn(features, labels, batch_size):
    def parser(example_proto):
        features = tf.parse_single_example(
                example_proto,
                features={
                    'molecule_fields_raw': tf.FixedLenFeature([], tf.string),
                    'U0s_raw': tf.FixedLenFeature([], tf.string)})
        X_1d = tf.decode_raw(features['molecule_fields_raw'], tf.float32)
        y_1d = tf.decode_raw(features['U0s_raw'], tf.float32)

        X = tf.reshape(X_1d, (20, 20, 20, 5))
        y = tf.reshape(y_1d, (1,))

        return X, y

    dataset = tf.data.TFRecordDataset(filenames[0])\
                     .map(parser)\
                     .repeat(3)\
                     .shuffle(50)\
                     .batch(10)

    
    return dataset

def model_fn(features, labels, mode, params):
    print(features)
    net = tf.feature_column.input_layer(features, params['feature_columns'])
    y_ = inference(net)
    if mode == tf.ModeKeys.PREDICT:
        predictions = {'U0': y_ }
        return tf.estimator.EstimatorSpec(mode, predictions=predictions)

    loss = tf.reduce_mean(tf.square(y_-y), name='loss')
    hartree = 627.5 #kcal/mol
    rme = tf.sqrt(loss)*hartree
    tf.summary.scalar('RME', rme)

    if mode == tf.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(mode, loss=loss, eval_metric_ops=rme)

    if mode == tf.ModeKeys.TRAIN:
        optimizer = tf.train.AdamOptimizer(params['lr'])
        train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)


ds = input_fn(0, 0, 0)
print(ds)

#distribution = tf.contrib.distribute.MirroredStrategy()
#config = tf.estimator.RunConfig(train_distribute=distribution)
#classifier = tf.estimator.Estimator(model_fn=model_fn, config=config)
#classifier.train(input_fn=input_fn)
#classifier.evaluate(input_fn=input_fn)

