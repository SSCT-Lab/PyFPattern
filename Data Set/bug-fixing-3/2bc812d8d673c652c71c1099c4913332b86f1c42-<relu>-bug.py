def relu(input):
    '\n    Relu takes one input data (Tensor) and produces one output data (Tensor)\n    where the rectified linear function, y = max(0, input), is applied to\n    the tensor elementwise.\n\n    .. math::\n\n        Out = \\max(0, input)\n\n    Args:\n        input (Variable): The input tensor.\n\n    Returns:\n        Variable: The output tensor with the same shape as input.\n\n    Examples:\n\n        .. code-block:: python\n\n            output = fluid.layers.relu(input)\n    '
    helper = LayerHelper('relu', **locals())
    dtype = helper.input_dtype(input_param_name='x')
    out = helper.create_tmp_variable(dtype)
    helper.append_op(type='relu', inputs={
        'X': x,
    }, outputs={
        'Out': out,
    })
    return out