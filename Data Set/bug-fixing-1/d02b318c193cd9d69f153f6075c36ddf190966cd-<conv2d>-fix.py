

def conv2d(input, num_filters, filter_size, stride=1, padding=0, dilation=1, groups=None, param_attr=None, bias_attr=None, use_cudnn=True, use_mkldnn=False, act=None, name=None):
    '\n    **Convlution2D Layer**\n\n    The convolution2D layer calculates the output based on the input, filter\n    and strides, paddings, dilations, groups parameters. Input(Input) and\n    Output(Output) are in NCHW format. Where N is batch size, C is the number of\n    channels, H is the height of the feature, and W is the width of the feature.\n    The details of convolution layer, please refer UFLDL\'s `convolution,\n    <http://ufldl.stanford.edu/tutorial/supervised/FeatureExtractionUsingConvolution/>`_ .\n    If bias attribution and activation type are provided, bias is added to the\n    output of the convolution, and the corresponding activation function is\n    applied to the final result.\n\n    For each input :math:`X`, the equation is:\n\n    .. math::\n\n        Out = \\sigma (W \\ast X + b)\n\n    In the above equation:\n\n    * :math:`X`: Input value, a tensor with NCHW format.\n    * :math:`W`: Filter value, a tensor with MCHW format.\n    * :math:`\\ast`: Convolution operation.\n    * :math:`b`: Bias value, a 2-D tensor with shape [M, 1].\n    * :math:`\\sigma`: Activation function.\n    * :math:`Out`: Output value, the shape of :math:`Out` and :math:`X` may be\n                   different.\n\n    Example:\n\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{out}, C_{in}, H_f, W_f)`\n\n        - Output:\n          Output shape: :math:`(N, C_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n            H_{out}&= \\frac{(H_{in} + 2 * paddings[0] - (dilations[0] * (H_f - 1) + 1))}{strides[0]} + 1 \\\\\n            W_{out}&= \\frac{(W_{in} + 2 * paddings[1] - (dilations[1] * (W_f - 1) + 1))}{strides[1]} + 1\n\n    Args:\n       input(Variable): The input image with [N, C, H, W] format.\n       num_filters(int): The number of filter. It is as same as the output\n           image channel.\n       filter_size(int|tuple|None): The filter size. If filter_size is a tuple,\n           it must contain two integers, (filter_size_H, filter_size_W).\n           Otherwise, the filter will be a square.\n       stride(int|tuple): The stride size. If stride is a tuple, it must\n           contain two integers, (stride_H, stride_W). Otherwise, the\n           stride_H = stride_W = stride. Default: stride = 1.\n       padding(int|tuple): The padding size. If padding is a tuple, it must\n           contain two integers, (padding_H, padding_W). Otherwise, the\n           padding_H = padding_W = padding. Default: padding = 0.\n       dilation(int|tuple): The dilation size. If dilation is a tuple, it must\n           contain two integers, (dilation_H, dilation_W). Otherwise, the\n           dilation_H = dilation_W = dilation. Default: dilation = 1.\n       groups(int): The groups number of the Conv2d Layer. According to grouped\n           convolution in Alex Krizhevsky\'s Deep CNN paper: when group=2,\n           the first half of the filters is only connected to the first half\n           of the input channels, while the second half of the filters is only\n           connected to the second half of the input channels. Default: groups=1\n       param_attr(ParamAttr): The parameters to the Conv2d Layer. Default: None\n       bias_attr(ParamAttr): Bias parameter for the Conv2d layer. Default: None\n       use_cudnn(bool): Use cudnn kernel or not, it is valid only when the cudnn\n           library is installed. Default: True\n       act(str): Activation type. Default: None\n       name(str|None): A name for this layer(optional). If set None, the layer\n           will be named automatically.\n\n    Returns:\n        Variable: The tensor variable storing the convolution and                   non-linearity activation result.\n\n    Raises:\n        ValueError: If the shapes of input, filter_size, stride, padding and\n                    groups mismatch.\n\n    Examples:\n        .. code-block:: python\n\n          data = fluid.layers.data(\n              name=\'data\', shape=[3, 32, 32], dtype=\'float32\')\n          conv2d = fluid.layers.conv2d(\n              input=data, num_filters=2, filter_size=3, act="relu")\n    '
    if (stride is None):
        stride = [1, 1]
    num_channels = input.shape[1]
    l_type = 'conv2d'
    if ((num_channels == groups) and ((num_filters % num_channels) == 0) and (not use_cudnn)):
        l_type = 'depthwise_conv2d'
    helper = LayerHelper(l_type, **locals())
    dtype = helper.input_dtype()
    if (groups is None):
        num_filter_channels = num_channels
    else:
        if ((num_channels % groups) != 0):
            raise ValueError('num_channels must be divisible by groups.')
        num_filter_channels = (num_channels / groups)
    filter_size = utils.convert_to_list(filter_size, 2, 'filter_size')
    stride = utils.convert_to_list(stride, 2, 'stride')
    padding = utils.convert_to_list(padding, 2, 'padding')
    dilation = utils.convert_to_list(dilation, 2, 'dilation')
    if (not isinstance(use_cudnn, bool)):
        raise ValueError('use_cudnn should be True or False')
    input_shape = input.shape
    filter_shape = ([num_filters, num_filter_channels] + filter_size)

    def _get_default_param_initializer():
        std = ((2.0 / ((filter_size[0] ** 2) * num_channels)) ** 0.5)
        return Normal(0.0, std, 0)
    filter_param = helper.create_parameter(attr=helper.param_attr, shape=filter_shape, dtype=dtype, default_initializer=_get_default_param_initializer())
    pre_bias = helper.create_tmp_variable(dtype)
    helper.append_op(type=l_type, inputs={
        'Input': input,
        'Filter': filter_param,
    }, outputs={
        'Output': pre_bias,
    }, attrs={
        'strides': stride,
        'paddings': padding,
        'dilations': dilation,
        'groups': groups,
        'use_cudnn': use_cudnn,
        'use_mkldnn': use_mkldnn,
    })
    pre_act = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    return helper.append_activation(pre_act)
