def sparse_softmax_cross_entropy_with_logits(logits, labels, name=None):
    'Computes sparse softmax cross entropy between `logits` and `labels`.\n\n  Measures the probability error in discrete classification tasks in which the\n  classes are mutually exclusive (each entry is in exactly one class).  For\n  example, each CIFAR-10 image is labeled with one and only one label: an image\n  can be a dog or a truck, but not both.\n\n  **NOTE:**  For this operation, the probability of a given label is considered\n  exclusive.  That is, soft classes are not allowed, and the `labels` vector\n  must provide a single specific index for the true class for each row of\n  `logits` (each minibatch entry).  For soft softmax classification with\n  a probability distribution for each entry, see\n  `softmax_cross_entropy_with_logits`.\n\n  **WARNING:** This op expects unscaled logits, since it performs a `softmax`\n  on `logits` internally for efficiency.  Do not call this op with the\n  output of `softmax`, as it will produce incorrect results.\n\n  `logits` and must have the shape `[batch_size, num_classes]`\n  and the dtype (either `float32` or `float64`).\n\n  `labels` must have the shape `[batch_size]` and the dtype `int64`.\n\n  Args:\n    logits: Unscaled log probabilities.\n    labels: Each entry `labels[i]` must be an index in `[0, num_classes)`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A 1-D `Tensor` of length `batch_size` of the same type as `logits` with the\n    softmax cross entropy loss.\n  '
    (cost, unused_backprop) = gen_nn_ops._sparse_softmax_cross_entropy_with_logits(logits, labels, name=name)
    return cost