def reduce_mean(input, dim=None, keep_dim=False, name=None):
    "\n    Computes the mean of the input tensor's elements along the given dimension.\n\n    Args:\n        input (Variable): The input variable which is a Tensor, the data type is float32,\n            float64, int32, int64.\n        dim (list|int, optional): The dimension along which the mean is computed. If\n            `None`, compute the mean over all elements of :attr:`input`\n            and return a variable with a single element, otherwise it\n            must be in the range :math:`[-rank(input), rank(input))`. If\n            :math:`dim[i] < 0`, the dimension to reduce is\n            :math:`rank(input) + dim[i]`.\n        keep_dim (bool, optional): Whether to reserve the reduced dimension in the\n            output Tensor. The result tensor will have one fewer dimension\n            than the :attr:`input` unless :attr:`keep_dim` is true, default \n            value is False.\n        name(str, optional): The default value is None.  Normally there is no need for\n            user to set this property.  For more information, please refer to :ref:`api_guide_Name`\n    \n    Returns:\n        Variable: Tensor, results of average on the specified dim of input tensor,\n        it's data type is the same as input's Tensor.\n    \n    Raises:\n        TypeError, if out data type is different with the input data type.\n    \n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            # x is a Tensor variable with following elements:\n            #    [[0.2, 0.3, 0.5, 0.9]\n            #     [0.1, 0.2, 0.6, 0.7]]\n            # Each example is followed by the correspending output tensor.\n            x = fluid.data(name='x', shape=[2, 4], dtype='float32')\n            fluid.layers.reduce_mean(x)  # [0.4375]\n            fluid.layers.reduce_mean(x, dim=0)  # [0.15, 0.25, 0.55, 0.8]\n            fluid.layers.reduce_mean(x, dim=-1)  # [0.475, 0.4]\n            fluid.layers.reduce_mean(x, dim=1, keep_dim=True)  # [[0.475], [0.4]]\n\n            # y is a Tensor variable with shape [2, 2, 2] and elements as below:\n            #      [[[1.0, 2.0], [3.0, 4.0]],\n            #      [[5.0, 6.0], [7.0, 8.0]]]\n            # Each example is followed by the correspending output tensor.\n            y = fluid.data(name='y', shape=[2, 2, 2], dtype='float32')\n            fluid.layers.reduce_mean(y, dim=[1, 2]) # [2.5, 6.5]\n            fluid.layers.reduce_mean(y, dim=[0, 1]) # [4.0, 5.0]\n    "
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
        outs = core.ops.reduce_mean(inputs, attrs)
        return outs['Out'][0]
    check_type_and_dtype(input, 'input', Variable, ['float32', 'float64', 'int32', 'int64'], 'reduce_mean')
    helper = LayerHelper('reduce_mean', **locals())
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype())
    helper.append_op(type='reduce_mean', inputs={
        'X': input,
    }, outputs={
        'Out': out,
    }, attrs=attrs)
    return out