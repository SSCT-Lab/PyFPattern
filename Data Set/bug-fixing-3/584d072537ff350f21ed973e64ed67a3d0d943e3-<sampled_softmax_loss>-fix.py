@tf_export('nn.sampled_softmax_loss')
def sampled_softmax_loss(weights, biases, labels, inputs, num_sampled, num_classes, num_true=1, sampled_values=None, remove_accidental_hits=True, partition_strategy='mod', name='sampled_softmax_loss', seed=None):
    'Computes and returns the sampled softmax training loss.\n\n  This is a faster way to train a softmax classifier over a huge number of\n  classes.\n\n  This operation is for training only.  It is generally an underestimate of\n  the full softmax loss.\n\n  A common use case is to use this method for training, and calculate the full\n  softmax loss for evaluation or inference. In this case, you must set\n  `partition_strategy="div"` for the two losses to be consistent, as in the\n  following example:\n\n  ```python\n  if mode == "train":\n    loss = tf.nn.sampled_softmax_loss(\n        weights=weights,\n        biases=biases,\n        labels=labels,\n        inputs=inputs,\n        ...,\n        partition_strategy="div")\n  elif mode == "eval":\n    logits = tf.matmul(inputs, tf.transpose(weights))\n    logits = tf.nn.bias_add(logits, biases)\n    labels_one_hot = tf.one_hot(labels, n_classes)\n    loss = tf.nn.softmax_cross_entropy_with_logits(\n        labels=labels_one_hot,\n        logits=logits)\n  ```\n\n  See our [Candidate Sampling Algorithms Reference]\n  (https://www.tensorflow.org/extras/candidate_sampling.pdf)\n\n  Also see Section 3 of [Jean et al., 2014](http://arxiv.org/abs/1412.2007)\n  ([pdf](http://arxiv.org/pdf/1412.2007.pdf)) for the math.\n\n  Args:\n    weights: A `Tensor` of shape `[num_classes, dim]`, or a list of `Tensor`\n        objects whose concatenation along dimension 0 has shape\n        [num_classes, dim].  The (possibly-sharded) class embeddings.\n    biases: A `Tensor` of shape `[num_classes]`.  The class biases.\n    labels: A `Tensor` of type `int64` and shape `[batch_size,\n        num_true]`. The target classes.  Note that this format differs from\n        the `labels` argument of `nn.softmax_cross_entropy_with_logits`.\n    inputs: A `Tensor` of shape `[batch_size, dim]`.  The forward\n        activations of the input network.\n    num_sampled: An `int`.  The number of classes to randomly sample per batch.\n    num_classes: An `int`. The number of possible classes.\n    num_true: An `int`.  The number of target classes per training example.\n    sampled_values: a tuple of (`sampled_candidates`, `true_expected_count`,\n        `sampled_expected_count`) returned by a `*_candidate_sampler` function.\n        (if None, we default to `log_uniform_candidate_sampler`)\n    remove_accidental_hits:  A `bool`.  whether to remove "accidental hits"\n        where a sampled class equals one of the target classes.  Default is\n        True.\n    partition_strategy: A string specifying the partitioning strategy, relevant\n        if `len(weights) > 1`. Currently `"div"` and `"mod"` are supported.\n        Default is `"mod"`. See `tf.nn.embedding_lookup` for more details.\n    name: A name for the operation (optional).\n    seed: random seed for candidate sampling. Default to None, which doesn\'t set\n        the op-level random seed for candidate sampling.\n\n  Returns:\n    A `batch_size` 1-D tensor of per-example sampled softmax losses.\n\n  '
    (logits, labels) = _compute_sampled_logits(weights=weights, biases=biases, labels=labels, inputs=inputs, num_sampled=num_sampled, num_classes=num_classes, num_true=num_true, sampled_values=sampled_values, subtract_log_q=True, remove_accidental_hits=remove_accidental_hits, partition_strategy=partition_strategy, name=name, seed=seed)
    labels = array_ops.stop_gradient(labels, name='labels_stop_gradient')
    sampled_losses = nn_ops.softmax_cross_entropy_with_logits_v2(labels=labels, logits=logits)
    return sampled_losses