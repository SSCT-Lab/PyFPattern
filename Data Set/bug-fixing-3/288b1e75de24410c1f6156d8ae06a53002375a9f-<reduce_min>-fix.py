def reduce_min(input, dim=None, keep_dim=False, name=None):
    "\n    Computes the minimum of tensor elements over the given dimension.\n\n    Args:\n        input (Variable): The input variable which is a Tensor, the data type is float32,\n            float64, int32, int64.\n        dim (list|int, optional): The dimensions along which the minimum is computed.\n            If :attr:`None`, compute the minimum over all elements of\n            :attr:`input` and return a Tensor variable with a single element,\n            otherwise must be in the range :math:`[-rank(input), rank(input))`.\n            If :math:`dim[i] < 0`, the dimension to reduce is :math:`rank + dim[i]`.\n        keep_dim (bool, optional): Whether to reserve the reduced dimension in the\n            output Tensor. The result tensor will have one fewer dimension\n            than the :attr:`input` unless :attr:`keep_dim` is true, default\n            value is False.\n        name(str, optional): The default value is None.  Normally there is no need for \n            user to set this property.  For more information, please refer to :ref:`api_guide_Name`\n\n    Returns:\n        Variable: Tensor, result of minimum on the specified dim of input tensor,\n        it's data type is the same as input's Tensor.\n\n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            # x is a Tensor variable with following elements:\n            #    [[0.2, 0.3, 0.5, 0.9]\n            #     [0.1, 0.2, 0.6, 0.7]]\n            # Each example is followed by the correspending output tensor.\n            x = fluid.data(name='x', shape=[2, 4], dtype='float32')\n            fluid.layers.reduce_min(x)  # [0.1]\n            fluid.layers.reduce_min(x, dim=0)  # [0.1, 0.2, 0.5, 0.7]\n            fluid.layers.reduce_min(x, dim=-1)  # [0.2, 0.1]\n            fluid.layers.reduce_min(x, dim=1, keep_dim=True)  # [[0.2], [0.1]]\n\n            # y is a Tensor variable with shape [2, 2, 2] and elements as below:\n            #      [[[1.0, 2.0], [3.0, 4.0]],\n            #      [[5.0, 6.0], [7.0, 8.0]]]\n            # Each example is followed by the correspending output tensor.\n            y = fluid.data(name='y', shape=[2, 2, 2], dtype='float32')\n            fluid.layers.reduce_min(y, dim=[1, 2]) # [1.0, 5.0]\n            fluid.layers.reduce_min(y, dim=[0, 1]) # [1.0, 2.0]\n    "
    helper = LayerHelper('reduce_min', **locals())
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype())
    if ((dim is not None) and (not isinstance(dim, list))):
        dim = [dim]
    helper.append_op(type='reduce_min', inputs={
        'X': input,
    }, outputs={
        'Out': out,
    }, attrs={
        'dim': (dim if ((dim != None) and (dim != [])) else [0]),
        'keep_dim': keep_dim,
        'reduce_all': (True if ((dim == None) or (dim == [])) else False),
    })
    return out