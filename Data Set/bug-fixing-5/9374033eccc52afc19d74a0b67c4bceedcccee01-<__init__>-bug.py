def __init__(self, source_vocab_size, target_vocab_size, buckets, size, num_layers, max_gradient_norm, batch_size, learning_rate, learning_rate_decay_factor, use_lstm=False, num_samples=512, forward_only=False, dtype=tf.float32):
    'Create the model.\n\n    Args:\n      source_vocab_size: size of the source vocabulary.\n      target_vocab_size: size of the target vocabulary.\n      buckets: a list of pairs (I, O), where I specifies maximum input length\n        that will be processed in that bucket, and O specifies maximum output\n        length. Training instances that have inputs longer than I or outputs\n        longer than O will be pushed to the next bucket and padded accordingly.\n        We assume that the list is sorted, e.g., [(2, 4), (8, 16)].\n      size: number of units in each layer of the model.\n      num_layers: number of layers in the model.\n      max_gradient_norm: gradients will be clipped to maximally this norm.\n      batch_size: the size of the batches used during training;\n        the model construction is independent of batch_size, so it can be\n        changed after initialization if this is convenient, e.g., for decoding.\n      learning_rate: learning rate to start with.\n      learning_rate_decay_factor: decay learning rate by this much when needed.\n      use_lstm: if true, we use LSTM cells instead of GRU cells.\n      num_samples: number of samples for sampled softmax.\n      forward_only: if set, we do not construct the backward pass in the model.\n      dtype: the data type to use to store internal variables.\n    '
    self.source_vocab_size = source_vocab_size
    self.target_vocab_size = target_vocab_size
    self.buckets = buckets
    self.batch_size = batch_size
    self.learning_rate = tf.Variable(float(learning_rate), trainable=False, dtype=dtype)
    self.learning_rate_decay_op = self.learning_rate.assign((self.learning_rate * learning_rate_decay_factor))
    self.global_step = tf.Variable(0, trainable=False)
    output_projection = None
    softmax_loss_function = None
    if ((num_samples > 0) and (num_samples < self.target_vocab_size)):
        w = tf.get_variable('proj_w', [size, self.target_vocab_size], dtype=dtype)
        w_t = tf.transpose(w)
        b = tf.get_variable('proj_b', [self.target_vocab_size], dtype=dtype)
        output_projection = (w, b)

        def sampled_loss(inputs, labels):
            labels = tf.reshape(labels, [(- 1), 1])
            local_w_t = tf.cast(w_t, tf.float32)
            local_b = tf.cast(b, tf.float32)
            local_inputs = tf.cast(inputs, tf.float32)
            return tf.cast(tf.nn.sampled_softmax_loss(local_w_t, local_b, local_inputs, labels, num_samples, self.target_vocab_size), dtype)
        softmax_loss_function = sampled_loss
    single_cell = tf.nn.rnn_cell.GRUCell(size)
    if use_lstm:
        single_cell = tf.nn.rnn_cell.BasicLSTMCell(size)
    cell = single_cell
    if (num_layers > 1):
        cell = tf.nn.rnn_cell.MultiRNNCell(([single_cell] * num_layers))

    def seq2seq_f(encoder_inputs, decoder_inputs, do_decode):
        return tf.nn.seq2seq.embedding_attention_seq2seq(encoder_inputs, decoder_inputs, cell, num_encoder_symbols=source_vocab_size, num_decoder_symbols=target_vocab_size, embedding_size=size, output_projection=output_projection, feed_previous=do_decode, dtype=dtype)
    self.encoder_inputs = []
    self.decoder_inputs = []
    self.target_weights = []
    for i in xrange(buckets[(- 1)][0]):
        self.encoder_inputs.append(tf.placeholder(tf.int32, shape=[batch_size], name='encoder{0}'.format(i)))
    for i in xrange((buckets[(- 1)][1] + 1)):
        self.decoder_inputs.append(tf.placeholder(tf.int32, shape=[batch_size], name='decoder{0}'.format(i)))
        self.target_weights.append(tf.placeholder(dtype, shape=[batch_size], name='weight{0}'.format(i)))
    targets = [self.decoder_inputs[(i + 1)] for i in xrange((len(self.decoder_inputs) - 1))]
    if forward_only:
        (self.outputs, self.losses) = tf.nn.seq2seq.model_with_buckets(self.encoder_inputs, self.decoder_inputs, targets, self.target_weights, buckets, (lambda x, y: seq2seq_f(x, y, True)), softmax_loss_function=softmax_loss_function)
        if (output_projection is not None):
            for b in xrange(len(buckets)):
                self.outputs[b] = [(tf.matmul(output, output_projection[0]) + output_projection[1]) for output in self.outputs[b]]
    else:
        (self.outputs, self.losses) = tf.nn.seq2seq.model_with_buckets(self.encoder_inputs, self.decoder_inputs, targets, self.target_weights, buckets, (lambda x, y: seq2seq_f(x, y, False)), softmax_loss_function=softmax_loss_function)
    params = tf.trainable_variables()
    if (not forward_only):
        self.gradient_norms = []
        self.updates = []
        opt = tf.train.GradientDescentOptimizer(self.learning_rate)
        for b in xrange(len(buckets)):
            gradients = tf.gradients(self.losses[b], params)
            (clipped_gradients, norm) = tf.clip_by_global_norm(gradients, max_gradient_norm)
            self.gradient_norms.append(norm)
            self.updates.append(opt.apply_gradients(zip(clipped_gradients, params), global_step=self.global_step))
    self.saver = tf.train.Saver(tf.all_variables())