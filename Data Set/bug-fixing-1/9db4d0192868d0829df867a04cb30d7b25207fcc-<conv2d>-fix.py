

def conv2d(input, num_filters, name=None, filter_size=[1, 1], act=None, groups=None, stride=[1, 1], padding=None, bias_attr=None, param_attr=None, main_program=None, startup_program=None):
    '\n    This function creates the op for a 2-dimensional Convolution.\n    This is performed using the parameters of filters(size, dimensionality etc)\n    , stride and other configurations for a Convolution operation.\n    This funciton can also append an activation on top of the\n    conv-2d output, if mentioned in the input parameters.\n    '
    helper = LayerHelper('conv2d', **locals())
    dtype = helper.input_dtype()
    num_channels = input.shape[1]
    if (groups is None):
        num_filter_channels = num_channels
    else:
        if ((num_channels % groups) != 0):
            raise ValueError('num_channels must be divisible by groups.')
        num_filter_channels = (num_channels / groups)
    if isinstance(filter_size, int):
        filter_size = [filter_size, filter_size]
    if isinstance(stride, int):
        stride = [stride, stride]
    if isinstance(padding, int):
        padding = [padding, padding]
    input_shape = input.shape
    filter_shape = ([num_filters, num_filter_channels] + filter_size)
    std = ((2.0 / ((filter_size[0] ** 2) * num_channels)) ** 0.5)
    filter = helper.create_parameter(attr=helper.param_attr, shape=filter_shape, dtype=dtype, initializer=NormalInitializer(0.0, std, 0))
    pre_bias = helper.create_tmp_variable(dtype)
    helper.append_op(type='conv2d', inputs={
        'Input': input,
        'Filter': filter,
    }, outputs={
        'Output': pre_bias,
    }, attrs={
        'strides': stride,
        'paddings': padding,
        'groups': groups,
    })
    pre_act = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    return helper.append_activation(pre_act)
