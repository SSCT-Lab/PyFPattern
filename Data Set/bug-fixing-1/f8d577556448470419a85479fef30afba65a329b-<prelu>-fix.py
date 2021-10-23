

def prelu(x, mode, param_attr=None, name=None):
    '\n    Equation:\n\n        y = \\max(0, x) + alpha \\min(0, x)\n\n    Args:\n        x (Variable): The input tensor.\n\t  param_attr(ParamAttr|None): The parameter attribute for the learnable\n                                    weight (alpha).\n        mode (string): The mode for weight sharing\n\t\t       all: all elements share same weight\n \t\t       channel:elements in a channel share same weight\n \t\t       element:each element has a weight\n\tname(str|None): A name for this layer(optional). If set None, the layer\n                        will be named automatically.\n\n    Returns:\n        Variable: The output tensor with the same shape as input.\n\n    Examples:\n\n        .. code-block:: python\n\n         x = fluid.layers.data(name="x", shape=[10,10], dtype="float32")\n            mode = \'channel\'\n            output = fluid.layers.prelu(x,mode)\n    '
    helper = LayerHelper('prelu', **locals())
    if (mode not in ['all', 'channel', 'element']):
        raise ValueError('mode should be one of all, channel, element.')
    alpha_shape = [1]
    if (mode == 'channel'):
        alpha_shape = [1, x.shape[1], 1, 1]
    elif (mode == 'element'):
        alpha_shape = x.shape
    dtype = helper.input_dtype(input_param_name='x')
    alpha = helper.create_parameter(attr=helper.param_attr, shape=alpha_shape, dtype='float32', is_bias=False, default_initializer=Constant(1.0))
    out = helper.create_variable_for_type_inference(dtype)
    helper.append_op(type='prelu', inputs={
        'X': x,
        'Alpha': alpha,
    }, attrs={
        'mode': mode,
    }, outputs={
        'Out': out,
    })
    return out
