

@tf_export('nn.dropout')
def dropout(x, keep_prob, noise_shape=None, seed=None, name=None):
    'Computes dropout.\n\n  With probability `keep_prob`, outputs the input element scaled up by\n  `1 / keep_prob`, otherwise outputs `0`.  The scaling is so that the expected\n  sum is unchanged.\n\n  By default, each element is kept or dropped independently.  If `noise_shape`\n  is specified, it must be\n  [broadcastable](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)\n  to the shape of `x`, and only dimensions with `noise_shape[i] == shape(x)[i]`\n  will make independent decisions.  For example, if `shape(x) = [k, l, m, n]`\n  and `noise_shape = [k, 1, 1, n]`, each batch and channel component will be\n  kept independently and each row and column will be kept or not kept together.\n\n  Args:\n    x: A floating point tensor.\n    keep_prob: A scalar `Tensor` with the same type as x. The probability\n      that each element is kept.\n    noise_shape: A 1-D `Tensor` of type `int32`, representing the\n      shape for randomly generated keep/drop flags.\n    seed: A Python integer. Used to create random seeds. See\n      `tf.set_random_seed`\n      for behavior.\n    name: A name for this operation (optional).\n\n  Returns:\n    A Tensor of the same shape of `x`.\n\n  Raises:\n    ValueError: If `keep_prob` is not in `(0, 1]` or if `x` is not a floating\n      point tensor.\n  '
    with ops.name_scope(name, 'dropout', [x]) as name:
        x = ops.convert_to_tensor(x, name='x')
        if (not x.dtype.is_floating):
            raise ValueError(("x has to be a floating point tensor since it's going to be scaled. Got a %s tensor instead." % x.dtype))
        if (isinstance(keep_prob, numbers.Real) and (not (0 < keep_prob <= 1))):
            raise ValueError(('keep_prob must be a scalar tensor or a float in the range (0, 1], got %g' % keep_prob))
        if (isinstance(keep_prob, float) and (keep_prob == 1)):
            return x
        if context.executing_eagerly():
            if isinstance(keep_prob, ops.EagerTensor):
                if (keep_prob.numpy() == 1):
                    return x
        else:
            keep_prob = ops.convert_to_tensor(keep_prob, dtype=x.dtype, name='keep_prob')
            keep_prob.get_shape().assert_is_compatible_with(tensor_shape.scalar())
            if (tensor_util.constant_value(keep_prob) == 1):
                return x
        noise_shape = _get_noise_shape(x, noise_shape)
        random_tensor = keep_prob
        random_tensor += random_ops.random_uniform(noise_shape, seed=seed, dtype=x.dtype)
        binary_tensor = math_ops.floor(random_tensor)
        ret = (math_ops.div(x, keep_prob) * binary_tensor)
        if (not context.executing_eagerly()):
            ret.set_shape(x.get_shape())
        return ret
