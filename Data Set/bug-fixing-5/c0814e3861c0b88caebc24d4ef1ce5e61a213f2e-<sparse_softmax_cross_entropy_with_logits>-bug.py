@tf_export('nn.sparse_softmax_cross_entropy_with_logits')
def sparse_softmax_cross_entropy_with_logits(_sentinel=None, labels=None, logits=None, name=None):
    'Computes sparse softmax cross entropy between `logits` and `labels`.\n\n  Measures the probability error in discrete classification tasks in which the\n  classes are mutually exclusive (each entry is in exactly one class).  For\n  example, each CIFAR-10 image is labeled with one and only one label: an image\n  can be a dog or a truck, but not both.\n\n  **NOTE:**  For this operation, the probability of a given label is considered\n  exclusive.  That is, soft classes are not allowed, and the `labels` vector\n  must provide a single specific index for the true class for each row of\n  `logits` (each minibatch entry).  For soft softmax classification with\n  a probability distribution for each entry, see\n  `softmax_cross_entropy_with_logits_v2`.\n\n  **WARNING:** This op expects unscaled logits, since it performs a `softmax`\n  on `logits` internally for efficiency.  Do not call this op with the\n  output of `softmax`, as it will produce incorrect results.\n\n  A common use case is to have logits and labels of shape\n  `[batch_size, num_classes]`, but higher dimensions are supported, in which\n  case the `dim`-th dimension is assumed to be of size `num_classes`.\n  `logits` must have the dtype of `float16`, `float32`, or `float64`, and\n  `labels` must have the dtype of `int32` or `int64`.\n\n  **Note that to avoid confusion, it is required to pass only named arguments to\n  this function.**\n\n  Args:\n    _sentinel: Used to prevent positional parameters. Internal, do not use.\n    labels: `Tensor` of shape `[d_0, d_1, ..., d_{r-1}]` (where `r` is rank of\n      `labels` and result) and dtype `int32` or `int64`. Each entry in `labels`\n      must be an index in `[0, num_classes)`. Other values will raise an\n      exception when this op is run on CPU, and return `NaN` for corresponding\n      loss and gradient rows on GPU.\n    logits: Unscaled log probabilities of shape\n      `[d_0, d_1, ..., d_{r-1}, num_classes]` and dtype `float16`, `float32`, or\n      `float64`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` of the same shape as `labels` and of the same type as `logits`\n    with the softmax cross entropy loss.\n\n  Raises:\n    ValueError: If logits are scalars (need to have rank >= 1) or if the rank\n      of the labels is not equal to the rank of the logits minus one.\n  '
    _ensure_xent_args('sparse_softmax_cross_entropy_with_logits', _sentinel, labels, logits)
    with ops.name_scope(name, 'SparseSoftmaxCrossEntropyWithLogits', [labels, logits]):
        labels = ops.convert_to_tensor(labels)
        logits = ops.convert_to_tensor(logits)
        precise_logits = (math_ops.cast(logits, dtypes.float32) if (dtypes.as_dtype(logits.dtype) == dtypes.float16) else logits)
        labels_static_shape = labels.get_shape()
        labels_shape = array_ops.shape(labels)
        static_shapes_fully_defined = (labels_static_shape.is_fully_defined() and logits.get_shape()[:(- 1)].is_fully_defined())
        if ((logits.get_shape().ndims is not None) and (logits.get_shape().ndims == 0)):
            raise ValueError(('Logits cannot be scalars - received shape %s.' % logits.get_shape()))
        if ((logits.get_shape().ndims is not None) and ((labels_static_shape.ndims is not None) and (labels_static_shape.ndims != (logits.get_shape().ndims - 1)))):
            raise ValueError(('Rank mismatch: Rank of labels (received %s) should equal rank of logits minus 1 (received %s).' % (labels_static_shape.ndims, logits.get_shape().ndims)))
        if (static_shapes_fully_defined and (labels_static_shape != logits.get_shape()[:(- 1)])):
            raise ValueError(('Shape mismatch: The shape of labels (received %s) should equal the shape of logits except for the last dimension (received %s).' % (labels_static_shape, logits.get_shape())))
        if (logits.get_shape().ndims == 2):
            (cost, _) = gen_nn_ops.sparse_softmax_cross_entropy_with_logits(precise_logits, labels, name=name)
            if (logits.dtype == dtypes.float16):
                return math_ops.cast(cost, dtypes.float16)
            else:
                return cost
        shape_checks = []
        if (not static_shapes_fully_defined):
            shape_checks.append(check_ops.assert_equal(array_ops.shape(labels), array_ops.shape(logits)[:(- 1)]))
        with ops.control_dependencies(shape_checks):
            num_classes = array_ops.shape(logits)[(array_ops.rank(logits) - 1)]
            precise_logits = array_ops.reshape(precise_logits, [(- 1), num_classes])
            labels = array_ops.reshape(labels, [(- 1)])
            (cost, _) = gen_nn_ops.sparse_softmax_cross_entropy_with_logits(precise_logits, labels, name=name)
            cost = array_ops.reshape(cost, labels_shape)
            cost.set_shape(labels_static_shape)
            if (logits.dtype == dtypes.float16):
                return math_ops.cast(cost, dtypes.float16)
            else:
                return cost