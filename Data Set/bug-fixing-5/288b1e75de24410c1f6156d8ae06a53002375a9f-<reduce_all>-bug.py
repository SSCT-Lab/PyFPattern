def reduce_all(input, dim=None, keep_dim=False, name=None):
    "\n    This OP computes the ``logical and`` of tensor elements over the given dimension, and output the result.\n\n    Args:\n        input (Variable): The input variable which is a Tensor or LoDTensor, the input data type should be `bool`.\n        dim (list|int|optional): The dimension along which the logical and is computed.\n            If :attr:`None`, compute the logical and over all elements of\n            :attr:`input` and return a Tensor variable with a single element,\n            otherwise must be in the range :math:`[-rank(input), rank(input))`.\n            If :math:`dim[i] < 0`, the dimension to reduce is :math:`rank + dim[i]`. The default value is None. \n        keep_dim (bool): Whether to reserve the reduced dimension in the\n            output Tensor. The result tensor will have one fewer dimension\n            than the :attr:`input` unless :attr:`keep_dim` is true. The default value is False.\n        name(str|None): A name for this layer(optional). If set None, the layer\n                       will be named automatically. The default value is None. \n\n    Returns: \n        Variable, the output data type is bool. : The reduced tensor variable with ``logical and`` in given dims.\n\n    Examples:\n        .. code-block:: python\n        \n            import paddle.fluid as fluid\n            import paddle.fluid.layers as layers\n            import numpy as np\n\n            # x is a bool Tensor variable with following elements:\n            #    [[True, False]\n            #     [True, True]]\n            x = layers.assign(np.array([[1, 0], [1, 1]], dtype='int32'))\n            x = layers.cast(x, 'bool')\n\n            out = layers.reduce_all(x)  # False \n            out = layers.reduce_all(x, dim=0)  # [True, False]\n            out = layers.reduce_all(x, dim=-1)  # [False, True]\n            # keep_dim=False, x.shape=(2,2), out.shape=(2,)\n\n            out = layers.reduce_all(x, dim=1, keep_dim=True)  # [[False], [True]]\n            # keep_dim=True, x.shape=(2,2), out.shape=(2,1)\n\n    "
    helper = LayerHelper('reduce_all', **locals())
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype())
    if ((dim is not None) and (not isinstance(dim, list))):
        dim = [dim]
    helper.append_op(type='reduce_all', inputs={
        'X': input,
    }, outputs={
        'Out': out,
    }, attrs={
        'dim': (dim if (dim != None) else [0]),
        'keep_dim': keep_dim,
        'reduce_all': (True if (dim == None) else False),
    })
    return out