@tf_export(v1=['nn.weighted_cross_entropy_with_logits'])
@deprecated_args(None, 'targets is deprecated, use labels instead', 'targets')
def weighted_cross_entropy_with_logits(labels=None, logits=None, pos_weight=None, name=None, targets=None):
    'Computes a weighted cross entropy.\n\n  This is like `sigmoid_cross_entropy_with_logits()` except that `pos_weight`,\n  allows one to trade off recall and precision by up- or down-weighting the\n  cost of a positive error relative to a negative error.\n  The usual cross-entropy cost is defined as:\n      labels * -log(sigmoid(logits)) +\n          (1 - labels) * -log(1 - sigmoid(logits))\n  A value `pos_weights > 1` decreases the false negative count, hence increasing\n  the recall.\n  Conversely setting `pos_weights < 1` decreases the false positive count and\n  increases the precision.\n  This can be seen from the fact that `pos_weight` is introduced as a\n  multiplicative coefficient for the positive labels term\n  in the loss expression:\n      labels * -log(sigmoid(logits)) * pos_weight +\n          (1 - labels) * -log(1 - sigmoid(logits))\n  For brevity, let `x = logits`, `z = labels`, `q = pos_weight`.\n  The loss is:\n        qz * -log(sigmoid(x)) + (1 - z) * -log(1 - sigmoid(x))\n      = qz * -log(1 / (1 + exp(-x))) + (1 - z) * -log(exp(-x) / (1 + exp(-x)))\n      = qz * log(1 + exp(-x)) + (1 - z) * (-log(exp(-x)) + log(1 + exp(-x)))\n      = qz * log(1 + exp(-x)) + (1 - z) * (x + log(1 + exp(-x))\n      = (1 - z) * x + (qz +  1 - z) * log(1 + exp(-x))\n      = (1 - z) * x + (1 + (q - 1) * z) * log(1 + exp(-x))\n  Setting `l = (1 + (q - 1) * z)`, to ensure stability and avoid overflow,\n  the implementation uses\n      (1 - z) * x + l * (log(1 + exp(-abs(x))) + max(-x, 0))\n  `logits` and `labels` must have the same type and shape.\n  Args:\n    labels: A `Tensor` of the same type and shape as `logits`.\n    logits: A `Tensor` of type `float32` or `float64`.\n    pos_weight: A coefficient to use on the positive examples.\n    name: A name for the operation (optional).\n    targets: Deprecated alias for labels.\n\n  Returns:\n    A `Tensor` of the same shape as `logits` with the componentwise\n    weighted logistic losses.\n  Raises:\n    ValueError: If `logits` and `labels` do not have the same shape.\n  '
    labels = deprecated_argument_lookup('labels', labels, 'targets', targets)
    return weighted_cross_entropy_with_logits_v2(labels, logits, pos_weight, name)