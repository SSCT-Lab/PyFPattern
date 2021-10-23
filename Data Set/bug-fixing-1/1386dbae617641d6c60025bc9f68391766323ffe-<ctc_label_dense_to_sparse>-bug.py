

def ctc_label_dense_to_sparse(labels, label_lengths):
    'Converts CTC labels from dense to sparse.\n\n    # Arguments\n        labels: dense CTC labels.\n        label_lengths: length of the labels.\n\n    # Returns\n        A sparse tensor representation of the lablels.\n    '
    label_shape = tf.shape(labels)
    num_batches_tns = tf.stack([label_shape[0]])
    max_num_labels_tns = tf.stack([label_shape[1]])

    def range_less_than(_, current_input):
        return (tf.expand_dims(tf.range(label_shape[1]), 0) < tf.fill(max_num_labels_tns, current_input))
    init = tf.cast(tf.fill([1, label_shape[1]], 0), tf.bool)
    dense_mask = functional_ops.scan(range_less_than, label_lengths, initializer=init, parallel_iterations=1)
    dense_mask = dense_mask[:, 0, :]
    label_array = tf.reshape(tf.tile(tf.range(0, label_shape[1]), num_batches_tns), label_shape)
    label_ind = tf.boolean_mask(label_array, dense_mask)
    batch_array = tf.transpose(tf.reshape(tf.tile(tf.range(0, label_shape[0]), max_num_labels_tns), reverse(label_shape, 0)))
    batch_ind = tf.boolean_mask(batch_array, dense_mask)
    indices = tf.transpose(tf.reshape(concatenate([batch_ind, label_ind], axis=0), [2, (- 1)]))
    vals_sparse = tf.gather_nd(labels, indices)
    return tf.SparseTensor(tf.to_int64(indices), vals_sparse, tf.to_int64(label_shape))
