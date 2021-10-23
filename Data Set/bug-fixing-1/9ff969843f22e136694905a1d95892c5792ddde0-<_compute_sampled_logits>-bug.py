

def _compute_sampled_logits(weights, biases, labels, inputs, num_sampled, num_classes, num_true=1, sampled_values=None, subtract_log_q=True, remove_accidental_hits=False, partition_strategy='mod', name=None, seed=None):
    'Helper function for nce_loss and sampled_softmax_loss functions.\n\n  Computes sampled output training logits and labels suitable for implementing\n  e.g. noise-contrastive estimation (see nce_loss) or sampled softmax (see\n  sampled_softmax_loss).\n\n  Note: In the case where num_true > 1, we assign to each target class\n  the target probability 1 / num_true so that the target probabilities\n  sum to 1 per-example.\n\n  Args:\n    weights: A `Tensor` of shape `[num_classes, dim]`, or a list of `Tensor`\n        objects whose concatenation along dimension 0 has shape\n        `[num_classes, dim]`.  The (possibly-partitioned) class embeddings.\n    biases: A `Tensor` of shape `[num_classes]`.  The (possibly-partitioned)\n        class biases.\n    labels: A `Tensor` of type `int64` and shape `[batch_size,\n        num_true]`. The target classes.  Note that this format differs from\n        the `labels` argument of `nn.softmax_cross_entropy_with_logits_v2`.\n    inputs: A `Tensor` of shape `[batch_size, dim]`.  The forward\n        activations of the input network.\n    num_sampled: An `int`.  The number of classes to randomly sample per batch.\n    num_classes: An `int`. The number of possible classes.\n    num_true: An `int`.  The number of target classes per training example.\n    sampled_values: a tuple of (`sampled_candidates`, `true_expected_count`,\n        `sampled_expected_count`) returned by a `*_candidate_sampler` function.\n        (if None, we default to `log_uniform_candidate_sampler`)\n    subtract_log_q: A `bool`.  whether to subtract the log expected count of\n        the labels in the sample to get the logits of the true labels.\n        Default is True.  Turn off for Negative Sampling.\n    remove_accidental_hits:  A `bool`.  whether to remove "accidental hits"\n        where a sampled class equals one of the target classes.  Default is\n        False.\n    partition_strategy: A string specifying the partitioning strategy, relevant\n        if `len(weights) > 1`. Currently `"div"` and `"mod"` are supported.\n        Default is `"mod"`. See `tf.nn.embedding_lookup` for more details.\n    name: A name for the operation (optional).\n    seed: random seed for candidate sampling. Default to None, which doesn\'t set\n        the op-level random seed for candidate sampling.\n  Returns:\n    out_logits: `Tensor` object with shape\n        `[batch_size, num_true + num_sampled]`, for passing to either\n        `nn.sigmoid_cross_entropy_with_logits` (NCE) or\n        `nn.softmax_cross_entropy_with_logits_v2` (sampled softmax).\n    out_labels: A Tensor object with the same shape as `out_logits`.\n  '
    if isinstance(weights, variables.PartitionedVariable):
        weights = list(weights)
    if (not isinstance(weights, list)):
        weights = [weights]
    with ops.name_scope(name, 'compute_sampled_logits', (weights + [biases, inputs, labels])):
        if (labels.dtype != dtypes.int64):
            labels = math_ops.cast(labels, dtypes.int64)
        labels_flat = array_ops.reshape(labels, [(- 1)])
        if (sampled_values is None):
            sampled_values = candidate_sampling_ops.log_uniform_candidate_sampler(true_classes=labels, num_true=num_true, num_sampled=num_sampled, unique=True, range_max=num_classes, seed=seed)
        (sampled, true_expected_count, sampled_expected_count) = (array_ops.stop_gradient(s) for s in sampled_values)
        sampled = math_ops.cast(sampled, dtypes.int64)
        all_ids = array_ops.concat([labels_flat, sampled], 0)
        all_w = embedding_ops.embedding_lookup(weights, all_ids, partition_strategy=partition_strategy)
        all_w = (all_w if (all_w.dtype == inputs.dtype) else math_ops.cast(all_w, inputs.dtype))
        true_w = array_ops.slice(all_w, [0, 0], array_ops.stack([array_ops.shape(labels_flat)[0], (- 1)]))
        sampled_w = array_ops.slice(all_w, array_ops.stack([array_ops.shape(labels_flat)[0], 0]), [(- 1), (- 1)])
        sampled_logits = math_ops.matmul(inputs, sampled_w, transpose_b=True)
        all_b = embedding_ops.embedding_lookup(biases, all_ids, partition_strategy=partition_strategy)
        all_b = (all_b if (all_b.dtype == inputs.dtype) else math_ops.cast(all_b, inputs.dtype))
        true_b = array_ops.slice(all_b, [0], array_ops.shape(labels_flat))
        sampled_b = array_ops.slice(all_b, array_ops.shape(labels_flat), [(- 1)])
        dim = array_ops.shape(true_w)[1:2]
        new_true_w_shape = array_ops.concat([[(- 1), num_true], dim], 0)
        row_wise_dots = math_ops.multiply(array_ops.expand_dims(inputs, 1), array_ops.reshape(true_w, new_true_w_shape))
        dots_as_matrix = array_ops.reshape(row_wise_dots, array_ops.concat([[(- 1)], dim], 0))
        true_logits = array_ops.reshape(_sum_rows(dots_as_matrix), [(- 1), num_true])
        true_b = array_ops.reshape(true_b, [(- 1), num_true])
        true_logits += true_b
        sampled_logits += sampled_b
        if remove_accidental_hits:
            acc_hits = candidate_sampling_ops.compute_accidental_hits(labels, sampled, num_true=num_true)
            (acc_indices, acc_ids, acc_weights) = acc_hits
            acc_indices_2d = array_ops.reshape(acc_indices, [(- 1), 1])
            acc_ids_2d_int32 = array_ops.reshape(math_ops.cast(acc_ids, dtypes.int32), [(- 1), 1])
            sparse_indices = array_ops.concat([acc_indices_2d, acc_ids_2d_int32], 1, 'sparse_indices')
            sampled_logits_shape = array_ops.concat([array_ops.shape(labels)[:1], array_ops.expand_dims(num_sampled, 0)], 0)
            if (sampled_logits.dtype != acc_weights.dtype):
                acc_weights = math_ops.cast(acc_weights, sampled_logits.dtype)
            sampled_logits += sparse_ops.sparse_to_dense(sparse_indices, sampled_logits_shape, acc_weights, default_value=0.0, validate_indices=False)
        if subtract_log_q:
            true_logits -= math_ops.log(true_expected_count)
            sampled_logits -= math_ops.log(sampled_expected_count)
        out_logits = array_ops.concat([true_logits, sampled_logits], 1)
        out_labels = array_ops.concat([(array_ops.ones_like(true_logits) / num_true), array_ops.zeros_like(sampled_logits)], 1)
        return (out_logits, out_labels)
