def affine_channel(x, scale=None, bias=None, data_layout='NCHW', name=None, act=None):
    '\n    Applies a separate affine transformation to each channel of the input.\n    Useful for replacing spatial batch norm with its equivalent fixed\n    transformation. The input also can be 2D tensor and applies a affine\n    transformation in second dimension.\n\n    Args:\n        x (Variable): Feature map input can be a 4D tensor with order NCHW\n            or NHWC. It also can be a 2D tensor and the affine transformation\n            is applied in the second dimension.\n        scale (Variable): 1D input of shape (C), the c-th element is the scale\n            factor of the affine transformation for the c-th channel of\n            the input.\n        bias (Variable): 1D input of shape (C), the c-th element is the bias\n            of the affine transformation for the c-th channel of the input.\n        data_layout (string, default NCHW): NCHW or NHWC. If input is 2D\n            tensor, you can ignore data_layout.\n        name (str, default None): The name of this layer.\n        act (str, default None): Activation to be applied to the output of this layer.\n\n    Returns:\n        out (Variable): A tensor of the same shape and data layout with x.\n    '
    helper = LayerHelper('affine_channel', **locals())
    if (name is None):
        out = helper.create_variable_for_type_inference(dtype=x.dtype)
    else:
        out = helper.create_variable(name=name, dtype=x.dtype, persistable=False)
    helper.append_op(type='affine_channel', inputs={
        'X': x,
        'Scale': scale,
        'Bias': bias,
    }, attrs={
        'data_layout': data_layout,
    }, outputs={
        'Out': out,
    })
    return helper.append_activation(out)