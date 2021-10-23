def log(input):
    '\n    Calculates the natural log of the given input tensor, element-wise.\n\n    .. math::\n\n        Out = \\ln(input)\n\n    Args:\n        input (Variable): Input tensor.\n\n    Returns:\n        Variable: The natural log of the input tensor computed element-wise.\n\n    Examples:\n\n        .. code-block:: python\n\n            output = fluid.layers.log(input)\n    '
    helper = LayerHelper('log', **locals())
    dtype = helper.input_dtype(input_param_name='x')
    out = helper.create_tmp_variable(dtype)
    helper.append_op(type='log', inputs={
        'X': x,
    }, outputs={
        'Out': out,
    })
    return out