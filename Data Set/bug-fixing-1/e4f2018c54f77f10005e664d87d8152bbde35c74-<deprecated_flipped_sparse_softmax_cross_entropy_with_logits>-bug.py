

def deprecated_flipped_sparse_softmax_cross_entropy_with_logits(logits, labels, name=None):
    'Computes sparse softmax cross entropy between `logits` and `labels`.\n\n  This function diffs from tf.nn.sparse_softmax_cross_entropy_with_logits only\n  in the argument order.\n\n  Measures the probability error in discrete classification tasks in which the\n  classes are mutually exclusive (each entry is in exactly one class).  For\n  example, each CIFAR-10 image is labeled with one and only one label: an image\n  can be a dog or a truck, but not both.\n\n  **NOTE:**  For this operation, the probability of a given label is considered\n  exclusive.  That is, soft classes are not allowed, and the `labels` vector\n  must provide a single specific index for the true class for each row of\n  `logits` (each minibatch entry).  For soft softmax classification with\n  a probability distribution for each entry, see\n  `softmax_cross_entropy_with_logits`.\n\n  **WARNING:** This op expects unscaled logits, since it performs a softmax\n  on `logits` internally for efficiency.  Do not call this op with the\n  output of `softmax`, as it will produce incorrect results.\n\n  A common use case is to have logits of shape `[batch_size, num_classes]` and\n  labels of shape `[batch_size]`. But higher dimensions are supported.\n\n  Args:\n\n    logits: Unscaled log probabilities of rank `r` and shape\n      `[d_0, d_1, ..., d_{r-2}, num_classes]` and dtype `float32` or `float64`.\n    labels: `Tensor` of shape `[d_0, d_1, ..., d_{r-2}]` and dtype `int32` or\n      `int64`. Each entry in `labels` must be an index in `[0, num_classes)`.\n      Other values will raise an exception when this op is run on CPU, and\n      return `NaN` for corresponding corresponding loss and gradient rows\n      on GPU.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` of the same shape as `labels` and of the same type as `logits`\n    with the softmax cross entropy loss.\n\n  Raises:\n    ValueError: If logits are scalars (need to have rank >= 1) or if the rank\n      of the labels is not equal to the rank of the labels minus one.\n  '
    return nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits, name=name)
