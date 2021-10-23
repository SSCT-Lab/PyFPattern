def transpose(x, perm, name=None):
    "\n    Permute the dimensions of `input` according to `perm`.\n\n    The `i`-th dimension  of the returned tensor will correspond to the\n    perm[i]-th dimension of `input`.\n\n    Args:\n        x (Variable): The input Tensor.\n        perm (list): A permutation of the dimensions of `input`.\n        name (str): The name of this layer. It is optional.\n\n    Returns:\n        Variable: A transposed Tensor.\n\n    Examples:\n        .. code-block:: python\n\n            x = fluid.layers.data(name='x', shape=[5, 10, 15], dtype='float32')\n            x_transposed = layers.transpose(x, perm=[1, 0, 2])\n    "
    if (len(perm) != len(x.shape)):
        raise ValueError("Input(perm) is the permutation of dimensions of Input(input). It's length shoud be equal to Input(input)'s rank.")
    for (idx, dim) in enumerate(perm):
        if (dim >= len(x.shape)):
            raise ValueError(("Each element in perm should be less than x's rank. %d-th element in perm is %d which accesses x's rank %d." % (idx, perm[idx], len(x.shape))))
    helper = LayerHelper('transpose', **locals())
    out = helper.create_variable_for_type_inference(x.dtype)
    x_shape = helper.create_variable_for_type_inference(x.dtype)
    helper.append_op(type='transpose2', inputs={
        'X': [x],
    }, outputs={
        'Out': [out],
        'XShape': [x_shape],
    }, attrs={
        'axis': perm,
    })
    return out