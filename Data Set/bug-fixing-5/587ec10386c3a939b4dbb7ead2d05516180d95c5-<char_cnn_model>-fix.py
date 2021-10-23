def char_cnn_model(features, labels, mode):
    'Character level convolutional neural network model to predict classes.'
    features_onehot = tf.one_hot(features[CHARS_FEATURE], 256)
    input_layer = tf.reshape(features_onehot, [(- 1), MAX_DOCUMENT_LENGTH, 256, 1])
    with tf.variable_scope('CNN_Layer1'):
        conv1 = tf.layers.conv2d(input_layer, filters=N_FILTERS, kernel_size=FILTER_SHAPE1, padding='VALID', activation=tf.nn.relu)
        pool1 = tf.layers.max_pooling2d(conv1, pool_size=POOLING_WINDOW, strides=POOLING_STRIDE, padding='SAME')
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])
    with tf.variable_scope('CNN_Layer2'):
        conv2 = tf.layers.conv2d(pool1, filters=N_FILTERS, kernel_size=FILTER_SHAPE2, padding='VALID')
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), axis=[1])
    logits = tf.layers.dense(pool2, MAX_LABEL, activation=None)
    predicted_classes = tf.argmax(logits, 1)
    if (mode == tf.estimator.ModeKeys.PREDICT):
        return tf.estimator.EstimatorSpec(mode=mode, predictions={
            'class': predicted_classes,
            'prob': tf.nn.softmax(logits),
        })
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
    if (mode == tf.estimator.ModeKeys.TRAIN):
        optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
        train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode, loss=loss, train_op=train_op)
    eval_metric_ops = {
        'accuracy': tf.metrics.accuracy(labels=labels, predictions=predicted_classes),
    }
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)