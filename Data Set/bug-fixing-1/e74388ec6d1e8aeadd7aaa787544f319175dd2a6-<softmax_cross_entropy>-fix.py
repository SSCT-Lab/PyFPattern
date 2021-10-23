

@tf_export(v1=['losses.softmax_cross_entropy'])
def softmax_cross_entropy(onehot_labels, logits, weights=1.0, label_smoothing=0, scope=None, loss_collection=ops.GraphKeys.LOSSES, reduction=Reduction.SUM_BY_NONZERO_WEIGHTS):
    "Creates a cross-entropy loss using tf.nn.softmax_cross_entropy_with_logits_v2.\n\n  `weights` acts as a coefficient for the loss. If a scalar is provided,\n  then the loss is simply scaled by the given value. If `weights` is a\n  tensor of shape `[batch_size]`, then the loss weights apply to each\n  corresponding sample.\n\n  If `label_smoothing` is nonzero, smooth the labels towards 1/num_classes:\n      new_onehot_labels = onehot_labels * (1 - label_smoothing)\n                          + label_smoothing / num_classes\n\n  Note that `onehot_labels` and `logits` must have the same shape,\n  e.g. `[batch_size, num_classes]`. The shape of `weights` must be\n  broadcastable to loss, whose shape is decided by the shape of `logits`.\n  In case the shape of `logits` is `[batch_size, num_classes]`, loss is\n  a `Tensor` of shape `[batch_size]`.\n\n  Args:\n    onehot_labels: One-hot-encoded labels.\n    logits: Logits outputs of the network.\n    weights: Optional `Tensor` that is broadcastable to loss.\n    label_smoothing: If greater than 0 then smooth the labels.\n    scope: the scope for the operations performed in computing the loss.\n    loss_collection: collection to which the loss will be added.\n    reduction: Type of reduction to apply to loss.\n\n  Returns:\n    Weighted loss `Tensor` of the same type as `logits`. If `reduction` is\n    `NONE`, this has shape `[batch_size]`; otherwise, it is scalar.\n\n  Raises:\n    ValueError: If the shape of `logits` doesn't match that of `onehot_labels`\n      or if the shape of `weights` is invalid or if `weights` is None.  Also if\n      `onehot_labels` or `logits` is None.\n\n  @compatibility(eager)\n  The `loss_collection` argument is ignored when executing eagerly. Consider\n  holding on to the return value or collecting losses via a `tf.keras.Model`.\n  @end_compatibility\n  "
    if (onehot_labels is None):
        raise ValueError('onehot_labels must not be None.')
    if (logits is None):
        raise ValueError('logits must not be None.')
    with ops.name_scope(scope, 'softmax_cross_entropy_loss', (logits, onehot_labels, weights)) as scope:
        logits = ops.convert_to_tensor(logits)
        onehot_labels = math_ops.cast(onehot_labels, logits.dtype)
        logits.get_shape().assert_is_compatible_with(onehot_labels.get_shape())
        if (label_smoothing > 0):
            num_classes = math_ops.cast(array_ops.shape(onehot_labels)[(- 1)], logits.dtype)
            smooth_positives = (1.0 - label_smoothing)
            smooth_negatives = (label_smoothing / num_classes)
            onehot_labels = ((onehot_labels * smooth_positives) + smooth_negatives)
        onehot_labels = array_ops.stop_gradient(onehot_labels, name='labels_stop_gradient')
        losses = nn.softmax_cross_entropy_with_logits_v2(labels=onehot_labels, logits=logits, name='xentropy')
        return compute_weighted_loss(losses, weights, scope, loss_collection, reduction=reduction)
