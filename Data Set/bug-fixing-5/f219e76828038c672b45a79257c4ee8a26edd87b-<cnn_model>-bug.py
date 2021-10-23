def cnn_model(features, target):
    '2 layer ConvNet to predict from sequence of words to a class.'
    target = tf.one_hot(target, 15, 1, 0)
    word_vectors = tf.contrib.layers.embed_sequence(features, vocab_size=n_words, embed_dim=EMBEDDING_SIZE, scope='words')
    word_vectors = tf.expand_dims(word_vectors, 3)
    with tf.variable_scope('CNN_Layer1'):
        conv1 = tf.contrib.layers.convolution2d(word_vectors, N_FILTERS, FILTER_SHAPE1, padding='VALID')
        conv1 = tf.nn.relu(conv1)
        pool1 = tf.nn.max_pool(conv1, ksize=[1, POOLING_WINDOW, 1, 1], strides=[1, POOLING_STRIDE, 1, 1], padding='SAME')
        pool1 = tf.transpose(pool1, [0, 1, 3, 2])
    with tf.variable_scope('CNN_Layer2'):
        conv2 = tf.contrib.layers.convolution2d(pool1, N_FILTERS, FILTER_SHAPE2, padding='VALID')
        pool2 = tf.squeeze(tf.reduce_max(conv2, 1), squeeze_dims=[1])
    logits = tf.contrib.layers.fully_connected(pool2, 15, activation_fn=None)
    loss = tf.contrib.losses.softmax_cross_entropy(logits, target)
    train_op = tf.contrib.layers.optimize_loss(loss, tf.contrib.framework.get_global_step(), optimizer='Adam', learning_rate=0.01)
    return ({
        'class': tf.argmax(logits, 1),
        'prob': tf.nn.softmax(logits),
    }, loss, train_op)