def _streaming_confusion_matrix_at_thresholds(predictions, labels, thresholds, weights=None, includes=None):
    "Computes true_positives, false_negatives, true_negatives, false_positives.\n\n  This function creates up to four local variables, `true_positives`,\n  `true_negatives`, `false_positives` and `false_negatives`.\n  `true_positive[i]` is defined as the total weight of values in `predictions`\n  above `thresholds[i]` whose corresponding entry in `labels` is `True`.\n  `false_negatives[i]` is defined as the total weight of values in `predictions`\n  at most `thresholds[i]` whose corresponding entry in `labels` is `True`.\n  `true_negatives[i]` is defined as the total weight of values in `predictions`\n  at most `thresholds[i]` whose corresponding entry in `labels` is `False`.\n  `false_positives[i]` is defined as the total weight of values in `predictions`\n  above `thresholds[i]` whose corresponding entry in `labels` is `False`.\n\n  For estimation of these metrics over a stream of data, for each metric the\n  function respectively creates an `update_op` operation that updates the\n  variable and returns its value.\n\n  If `weights` is `None`, weights default to 1. Use weights of 0 to mask values.\n\n  Args:\n    predictions: A floating point `Tensor` of arbitrary shape and whose values\n      are in the range `[0, 1]`.\n    labels: A `Tensor` whose shape matches `predictions`. `labels` will be cast\n      to `bool`.\n    thresholds: A python list or tuple of float thresholds in `[0, 1]`.\n    weights: Optional `Tensor` whose rank is either 0, or the same rank as\n      `labels`, and must be broadcastable to `labels` (i.e., all dimensions\n      must be either `1`, or the same as the corresponding `labels`\n      dimension).\n    includes: Tuple of keys to return, from 'tp', 'fn', 'tn', fp'. If `None`,\n      default to all four.\n\n  Returns:\n    values: Dict of variables of shape `[len(thresholds)]`. Keys are from\n        `includes`.\n    update_ops: Dict of operations that increments the `values`. Keys are from\n        `includes`.\n\n  Raises:\n    ValueError: If `predictions` and `labels` have mismatched shapes, or if\n      `weights` is not `None` and its shape doesn't match `predictions`, or if\n      `includes` contains invalid keys.\n  "
    all_includes = ('tp', 'fn', 'tn', 'fp')
    if (includes is None):
        includes = all_includes
    else:
        for include in includes:
            if (include not in all_includes):
                raise ValueError(('Invalid key: %s.' % include))
    (predictions, labels, weights) = metrics_impl._remove_squeezable_dimensions(predictions, labels, weights)
    predictions.get_shape().assert_is_compatible_with(labels.get_shape())
    num_thresholds = len(thresholds)
    predictions_2d = array_ops.reshape(predictions, [(- 1), 1])
    labels_2d = array_ops.reshape(math_ops.cast(labels, dtype=dtypes.bool), [1, (- 1)])
    num_predictions = predictions_2d.get_shape().as_list()[0]
    if (num_predictions is None):
        num_predictions = array_ops.shape(predictions_2d)[0]
    thresh_tiled = array_ops.tile(array_ops.expand_dims(array_ops.constant(thresholds), [1]), array_ops.stack([1, num_predictions]))
    pred_is_pos = math_ops.greater(array_ops.tile(array_ops.transpose(predictions_2d), [num_thresholds, 1]), thresh_tiled)
    if (('fn' in includes) or ('tn' in includes)):
        pred_is_neg = math_ops.logical_not(pred_is_pos)
    label_is_pos = array_ops.tile(labels_2d, [num_thresholds, 1])
    if (('fp' in includes) or ('tn' in includes)):
        label_is_neg = math_ops.logical_not(label_is_pos)
    if (weights is not None):
        broadcast_weights = weights_broadcast_ops.broadcast_weights(math_ops.to_float(weights), predictions)
        weights_tiled = array_ops.tile(array_ops.reshape(broadcast_weights, [1, (- 1)]), [num_thresholds, 1])
        thresh_tiled.get_shape().assert_is_compatible_with(weights_tiled.get_shape())
    else:
        weights_tiled = None
    values = {
        
    }
    update_ops = {
        
    }
    if ('tp' in includes):
        true_positives = metrics_impl.metric_variable([num_thresholds], dtypes.float32, name='true_positives')
        is_true_positive = math_ops.to_float(math_ops.logical_and(label_is_pos, pred_is_pos))
        if (weights_tiled is not None):
            is_true_positive *= weights_tiled
        update_ops['tp'] = state_ops.assign_add(true_positives, math_ops.reduce_sum(is_true_positive, 1))
        values['tp'] = true_positives
    if ('fn' in includes):
        false_negatives = metrics_impl.metric_variable([num_thresholds], dtypes.float32, name='false_negatives')
        is_false_negative = math_ops.to_float(math_ops.logical_and(label_is_pos, pred_is_neg))
        if (weights_tiled is not None):
            is_false_negative *= weights_tiled
        update_ops['fn'] = state_ops.assign_add(false_negatives, math_ops.reduce_sum(is_false_negative, 1))
        values['fn'] = false_negatives
    if ('tn' in includes):
        true_negatives = metrics_impl.metric_variable([num_thresholds], dtypes.float32, name='true_negatives')
        is_true_negative = math_ops.to_float(math_ops.logical_and(label_is_neg, pred_is_neg))
        if (weights_tiled is not None):
            is_true_negative *= weights_tiled
        update_ops['tn'] = state_ops.assign_add(true_negatives, math_ops.reduce_sum(is_true_negative, 1))
        values['tn'] = true_negatives
    if ('fp' in includes):
        false_positives = metrics_impl.metric_variable([num_thresholds], dtypes.float32, name='false_positives')
        is_false_positive = math_ops.to_float(math_ops.logical_and(label_is_neg, pred_is_pos))
        if (weights_tiled is not None):
            is_false_positive *= weights_tiled
        update_ops['fp'] = state_ops.assign_add(false_positives, math_ops.reduce_sum(is_false_positive, 1))
        values['fp'] = false_positives
    return (values, update_ops)