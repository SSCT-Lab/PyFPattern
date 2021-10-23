def log(x):
    '\n    Calculates the natural log of the given input tensor, element-wise.\n\n    .. math::\n\n        Out = \\ln(x)\n\n    Args:\n        x (Variable): Input tensor.\n\n    Returns:\n        Variable: The natural log of the input tensor computed element-wise.\n\n    Examples:\n\n        .. code-block:: python\n\n            output = fluid.layers.log(x)\n    '
    helper = LayerHelper('log', **locals())
    dtype = helper.input_dtype()
    out = helper.create_tmp_variable(dtype)
    helper.append_op(type='log', inputs={
        'X': input,
    }, outputs={
        'Out': out,
    })
    return out