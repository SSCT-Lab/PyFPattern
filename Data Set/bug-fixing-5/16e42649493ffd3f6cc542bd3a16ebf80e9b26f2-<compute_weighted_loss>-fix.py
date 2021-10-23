def compute_weighted_loss(losses, sample_weight=None, reduction=losses_impl.ReductionV2.SUM_OVER_BATCH_SIZE, name=None):
    'Computes the weighted loss.\n\n  Args:\n    losses: `Tensor` of shape `[batch_size, d1, ... dN]`.\n    sample_weight: Optional `Tensor` whose rank is either 0, or the same rank as\n      `losses`, or be broadcastable to `losses`.\n    reduction: Type of `tf.losses.Reduction` to apply to loss. Default value is\n      `SUM_OVER_BATCH_SIZE`.\n    name: Optional name for the op.\n\n  Raises:\n    ValueError: If the shape of `sample_weight` is not compatible with `losses`.\n\n  Returns:\n    Weighted loss `Tensor` of the same type as `losses`. If `reduction` is\n    `NONE`, this has the same shape as `losses`; otherwise, it is scalar.\n  '
    losses_impl.ReductionV2.validate(reduction)
    if (sample_weight is None):
        sample_weight = 1.0
    with ops.name_scope(name, 'weighted_loss', (losses, sample_weight)):
        ops.get_default_graph()._last_loss_reduction = reduction
        (losses, _, sample_weight) = squeeze_or_expand_dimensions(losses, None, sample_weight)
        losses = ops.convert_to_tensor(losses)
        input_dtype = losses.dtype
        losses = math_ops.cast(losses, dtypes.float32)
        sample_weight = math_ops.cast(sample_weight, dtypes.float32)
        try:
            sample_weight = weights_broadcast_ops.broadcast_weights(sample_weight, losses)
        except ValueError:
            ndim = K.ndim(losses)
            weight_ndim = K.ndim(sample_weight)
            losses = K.mean(losses, axis=list(range(weight_ndim, ndim)))
        sample_weight.get_shape().assert_is_compatible_with(losses.get_shape())
        weighted_losses = math_ops.multiply(losses, sample_weight)
        loss = _reduce_weighted_loss(weighted_losses, reduction)
        loss = math_ops.cast(loss, input_dtype)
        return loss