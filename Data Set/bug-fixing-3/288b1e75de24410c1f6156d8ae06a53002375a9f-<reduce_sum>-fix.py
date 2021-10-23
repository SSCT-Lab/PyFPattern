def reduce_sum(input, dim=None, keep_dim=False, name=None):
    "\n    Computes the sum of tensor elements over the given dimension.\n\n    Args:\n        input (Variable): The input variable which is a Tensor, the data type is float32,\n            float64, int32, int64.\n        dim (list|int, optional): The dimensions along which the sum is performed. If\n            :attr:`None`, sum all elements of :attr:`input` and return a\n            Tensor variable with a single element, otherwise must be in the\n            range :math:`[-rank(input), rank(input))`. If :math:`dim[i] < 0`,\n            the dimension to reduce is :math:`rank + dim[i]`.\n        keep_dim (bool, optional): Whether to reserve the reduced dimension in the\n            output Tensor. The result tensor will have one fewer dimension\n            than the :attr:`input` unless :attr:`keep_dim` is true, default\n            value is False.\n        name(str, optional): The default value is None.  Normally there is no need for\n            user to set this property.  For more information, please refer to :ref:`api_guide_Name`\n\n    Returns:\n        Variable: Tensor, results of summation operation on the specified dim of input tensor,\n        it's data type is the same as input's Tensor.\n\n    Raises:\n        TypeError, if out data type is different with the input data type.\n    \n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            # x is a Tensor variable with following elements:\n            #    [[0.2, 0.3, 0.5, 0.9]\n            #     [0.1, 0.2, 0.6, 0.7]]\n            # Each example is followed by the corresponding output tensor.\n            x = fluid.data(name='x', shape=[2, 4], dtype='float32')\n            fluid.layers.reduce_sum(x)  # [3.5]\n            fluid.layers.reduce_sum(x, dim=0)  # [0.3, 0.5, 1.1, 1.6]\n            fluid.layers.reduce_sum(x, dim=-1)  # [1.9, 1.6]\n            fluid.layers.reduce_sum(x, dim=1, keep_dim=True)  # [[1.9], [1.6]]\n\n            # y is a Tensor variable with shape [2, 2, 2] and elements as below:\n            #      [[[1, 2], [3, 4]],\n            #      [[5, 6], [7, 8]]]\n            # Each example is followed by the corresponding output tensor.\n            y = fluid.data(name='y', shape=[2, 2, 2], dtype='float32')\n            fluid.layers.reduce_sum(y, dim=[1, 2]) # [10, 26]\n            fluid.layers.reduce_sum(y, dim=[0, 1]) # [16, 20]\n\n    "
    if ((dim is not None) and (not isinstance(dim, list))):
        dim = [dim]
    attrs = {
        'dim': (dim if ((dim != None) and (dim != [])) else [0]),
        'keep_dim': keep_dim,
        'reduce_all': (True if ((dim == None) or (dim == [])) else False),
    }
    if in_dygraph_mode():
        inputs = {
            'X': [input],
        }
        outs = core.ops.reduce_sum(inputs, attrs)
        return outs['Out'][0]
    check_type_and_dtype(input, 'input', Variable, ['float32', 'float64', 'int32', 'int64'], 'reduce_sum')
    helper = LayerHelper('reduce_sum', **locals())
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype())
    helper.append_op(type='reduce_sum', inputs={
        'X': input,
    }, outputs={
        'Out': out,
    }, attrs=attrs)
    return out