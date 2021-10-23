@tf_export('nn.batch_normalization')
def batch_normalization(x, mean, variance, offset, scale, variance_epsilon, name=None):
    "Batch normalization.\n\n  Normalizes a tensor by `mean` and `variance`, and applies (optionally) a\n  `scale` \\\\(\\gamma\\\\) to it, as well as an `offset` \\\\(\\beta\\\\):\n\n  \\\\(\\frac{\\gamma(x-\\mu)}{\\sigma}+\\beta\\\\)\n\n  `mean`, `variance`, `offset` and `scale` are all expected to be of one of two\n  shapes:\n\n    * In all generality, they can have the same number of dimensions as the\n      input `x`, with identical sizes as `x` for the dimensions that are not\n      normalized over (the 'depth' dimension(s)), and dimension 1 for the\n      others which are being normalized over.\n      `mean` and `variance` in this case would typically be the outputs of\n      `tf.nn.moments(..., keepdims=True)` during training, or running averages\n      thereof during inference.\n    * In the common case where the 'depth' dimension is the last dimension in\n      the input tensor `x`, they may be one dimensional tensors of the same\n      size as the 'depth' dimension.\n      This is the case for example for the common `[batch, depth]` layout of\n      fully-connected layers, and `[batch, height, width, depth]` for\n      convolutions.\n      `mean` and `variance` in this case would typically be the outputs of\n      `tf.nn.moments(..., keepdims=False)` during training, or running averages\n      thereof during inference.\n\n  See equation 11 in Algorithm 2 of source: [Batch Normalization: Accelerating Deep Network Training by\n  Reducing Internal Covariate Shift; S. Ioffe, C. Szegedy]\n  (http://arxiv.org/abs/1502.03167).\n\n  Args:\n    x: Input `Tensor` of arbitrary dimensionality.\n    mean: A mean `Tensor`.\n    variance: A variance `Tensor`.\n    offset: An offset `Tensor`, often denoted \\\\(\\beta\\\\) in equations, or\n      None. If present, will be added to the normalized tensor.\n    scale: A scale `Tensor`, often denoted \\\\(\\gamma\\\\) in equations, or\n      `None`. If present, the scale is applied to the normalized tensor.\n    variance_epsilon: A small float number to avoid dividing by 0.\n    name: A name for this operation (optional).\n\n  Returns:\n    Normalized, scaled, offset tensor.\n  "
    with ops.name_scope(name, 'batchnorm', [x, mean, variance, scale, offset]):
        inv = math_ops.rsqrt((variance + variance_epsilon))
        if (scale is not None):
            inv *= scale
        return ((x * math_ops.cast(inv, x.dtype)) + math_ops.cast(((offset - (mean * inv)) if (offset is not None) else ((- mean) * inv)), x.dtype))