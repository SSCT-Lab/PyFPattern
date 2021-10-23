def reshape(x, shape, actual_shape=None, act=None, inplace=True, name=None):
    "\n    Gives a new shape to the input Tensor without changing its data.\n\n    The target shape can be given by :attr:`shape` or :attr:`actual_shape`.\n    :attr:`shape` is a list of integer while :attr:`actual_shape` is a tensor\n    variable. :attr:`actual_shape` has a higher priority than :attr:`shape`\n    if it is provided, while :attr:`shape` still should be set correctly to\n    gurantee shape inference in compile-time.\n\n    Some tricks exist when specifying the target shape.\n\n    1. -1 means the value of this dimension is inferred from the total element\n    number of x and remaining dimensions. Thus one and only one dimension can\n    be set -1.\n\n    2. 0 means the actual dimension value is going to be copied from the\n    corresponding dimension of x. The indice of 0s in shape can not exceed\n    Rank(X).\n\n    Here are some examples to explain it.\n\n    1. Given a 3-D tensor x with a shape [2, 4, 6], and the target shape\n    is [6, 8], the reshape operator will transform x into a 2-D tensor with\n    shape [6, 8] and leaving x's data unchanged.\n\n    2. Given a 3-D tensor x with a shape [2, 4, 6], and the target shape\n    specified is [2, 3, -1, 2], the reshape operator will transform x into a\n    4-D tensor with shape [2, 3, 4, 2] and leaving x's data unchanged. In this\n    case, one dimension of the target shape is set to -1, the value of this\n    dimension is inferred from the total element number of x and remaining\n    dimensions.\n\n    3. Given a 3-D tensor x with a shape [2, 4, 6], and the target shape\n    is [-1, 0, 3, 2], the reshape operator will transform x into a 4-D tensor\n    with shape [2, 4, 3, 2] and leaving x's data unchanged. In this case,\n    besides -1, 0 means the actual dimension value is going to be copied from\n    the corresponding dimension of x.\n\n    Args:\n        x(variable): The input tensor.\n        shape(list): The new shape. At most one dimension of the new shape can\n                     be -1.\n        actual_shape(variable): An optional input. If provided, reshape\n                                according to this given shape rather than\n                                :attr:`shape` specifying shape. That is to\n                                say :attr:`actual_shape` has a higher priority\n                                than :attr:`shape`.\n        act (str): The non-linear activation to be applied to output variable.\n        inplace(bool): If this flag is set true, the output\n                       shares data with input without copying, otherwise\n                       a new output tensor is created\n                       whose data is copied from input x.\n        name (str): The name of this layer. It is optional.\n\n    Returns:\n        Variable: The output tensor.\n\n    Raises:\n        TypeError: if actual_shape is neither Variable nor None.\n\n    Examples:\n        .. code-block:: python\n\n            data = fluid.layers.data(\n                name='data', shape=[2, 4, 6], dtype='float32')\n            reshaped = fluid.layers.reshape(\n                x=data, shape=[-1, 0, 3, 2], act='tanh', inplace=True)\n    "
    if (not (isinstance(shape, list) or isinstance(shape, tuple))):
        raise ValueError('Input shape must be a python lsit or tuple.')
    inputs = {
        'X': x,
    }
    if isinstance(actual_shape, Variable):
        inputs['Shape'] = actual_shape
    elif (actual_shape is not None):
        raise TypeError('actual_shape should either be Variable or None')
    unk_dim_idx = (- 1)
    for (dim_idx, dim_size) in enumerate(shape):
        if (dim_size == (- 1)):
            assert (unk_dim_idx == (- 1)), 'Only one dimension in shape can be unknown.'
            unk_dim_idx = dim_idx
        elif (dim_size == 0):
            assert (dim_idx < len(x.shape)), 'The indice of 0s in shape can not exceed Rank(X).'
        else:
            assert (dim_size > 0), 'Each dimension size given in shape must not be negtive except one unknown dimension.'
    helper = LayerHelper('reshape', **locals())
    reshaped = helper.create_tmp_variable(dtype=x.dtype)
    helper.append_op(type='reshape', inputs=inputs, attrs={
        'shape': shape,
        'inplace': inplace,
    }, outputs={
        'Out': reshaped,
    })
    return helper.append_activation(reshaped)