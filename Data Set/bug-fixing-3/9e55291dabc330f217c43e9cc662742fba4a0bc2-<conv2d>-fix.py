def conv2d(input, num_filters, filter_size, stride=1, padding=0, dilation=1, groups=None, param_attr=None, bias_attr=None, use_cudnn=True, act=None, name=None, data_format='NCHW'):
    '\n    The convolution2D layer calculates the output based on the input, filter\n    and strides, paddings, dilations, groups parameters. Input and\n    Output are in NCHW or NHWC format, where N is batch size, C is the number of\n    channels, H is the height of the feature, and W is the width of the feature.\n    Filter is in MCHW format, where M is the number of output image channels,\n    C is the number of input image channels, H is the height of the filter,\n    and W is the width of the filter. If the groups is greater than 1,\n    C will equal the number of input image channels divided by the groups.\n    Please refer to UFLDL\'s `convolution\n    <http://ufldl.stanford.edu/tutorial/supervised/FeatureExtractionUsingConvolution/>`_\n    for more details.\n    If bias attribution and activation type are provided, bias is added to the\n    output of the convolution, and the corresponding activation function is\n    applied to the final result.\n\n    For each input :math:`X`, the equation is:\n\n    .. math::\n\n        Out = \\sigma (W \\ast X + b)\n\n    Where:\n\n    * :math:`X`: Input value, a tensor with NCHW or NHWC format.\n    * :math:`W`: Filter value, a tensor with MCHW format.\n    * :math:`\\ast`: Convolution operation.\n    * :math:`b`: Bias value, a 2-D tensor with shape [M, 1].\n    * :math:`\\sigma`: Activation function.\n    * :math:`Out`: Output value, the shape of :math:`Out` and :math:`X` may be different.\n\n    Example:\n\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{out}, C_{in}, H_f, W_f)`\n\n        - Output:\n\n          Output shape: :math:`(N, C_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n            H_{out}&= \\frac{(H_{in} + 2 * paddings[0] - (dilations[0] * (H_f - 1) + 1))}{strides[0]} + 1 \\\\\n            W_{out}&= \\frac{(W_{in} + 2 * paddings[1] - (dilations[1] * (W_f - 1) + 1))}{strides[1]} + 1\n\n    Args:\n        input (Variable): The input is 4-D Tensor with shape [N, C, H, W], the data type \n            of input is float16 or float32 or float64.\n        num_filters(int): The number of filter. It is as same as the output\n            image channel.\n        filter_size (int|tuple): The filter size. If filter_size \n            is a tuple, it must contain two integers, (filter_size_height, \n            filter_size_width). Otherwise, filter_size_height = filter_size_width =            filter_size.\n        stride (int|tuple): The stride size. It means the stride in convolution. \n            If stride is a tuple, it must contain two integers, (stride_height, stride_width). \n            Otherwise, stride_height = stride_width = stride. Default: stride = 1.\n        padding (string|int|list|tuple): The padding size. It means the number of zero-paddings\n            on both sides for each dimention.If `padding` is a string, either \'VALID\' or\n            \'SAME\' which is the padding algorithm. If padding size is a tuple or list,\n            it could be in three forms: `[pad_height, pad_width]` or\n            `[pad_height_top, pad_height_bottom, pad_width_left, pad_width_right]`, and when \n            `data_format` is `"NCHW"`, `padding` can be in the form `[[0,0], [0,0], \n            [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right]]`.\n            when `data_format` is `"NHWC"`, `pool_padding` can be in the form\n            `[[0,0], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right], [0,0]]`.\n            Default: padding = 0.\n        dilation (int|tuple): The dilation size. It means the spacing between the kernel\n            points. If dilation is a tuple, it must contain two integers, (dilation_height, \n            dilation_width). Otherwise, dilation_height = dilation_width = dilation. \n            Default: dilation = 1.\n        groups (int): The groups number of the Conv2d Layer. According to grouped\n            convolution in Alex Krizhevsky\'s Deep CNN paper: when group=2,\n            the first half of the filters is only connected to the first half\n            of the input channels, while the second half of the filters is only\n            connected to the second half of the input channels. Default: groups=1.\n        param_attr (ParamAttr|None): The parameter attribute for learnable parameters/weights\n            of conv2d. If it is set to None or one attribute of ParamAttr, conv2d\n            will create ParamAttr as param_attr. If the Initializer of the param_attr\n            is not set, the parameter is initialized with :math:`Normal(0.0, std)`,\n            and the :math:`std` is :math:`(\\frac{2.0 }{filter\\_elem\\_num})^{0.5}`. Default: None.\n        bias_attr (ParamAttr|bool|None): The parameter attribute for the bias of conv2d.\n            If it is set to False, no bias will be added to the output units.\n            If it is set to None or one attribute of ParamAttr, conv2d\n            will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n            is not set, the bias is initialized zero. Default: None.\n        use_cudnn (bool): Use cudnn kernel or not, it is valid only when the cudnn\n            library is installed. Default: True\n        act (str): Activation type, if it is set to None, activation is not appended.\n            Default: None\n        name(str|None): For detailed information, please refer \n           to :ref:`api_guide_Name`. Usually name is no need to set and \n           None by default.\n        data_format (str): The data format of the input and output data. An optional string from: `"NCHW"`, `"NHWC"`.\n            The default is `"NCHW"`. When it is `"NCHW"`, the data is stored in the order of:\n            `[batch_size, input_channels, input_height, input_width]`.\n\n    Returns:\n        A Variable holding Tensor representing the conv2d, whose data type is the \n        same with input. If act is None, the tensor variable storing the convolution \n        result, and if act is not None, the tensor variable storing convolution \n        and non-linearity activation result.\n\n    Examples:\n        .. code-block:: python\n\n          import paddle.fluid as fluid\n          data = fluid.data(name=\'data\', shape=[None, 3, 32, 32], dtype=\'float32\')\n          conv2d = fluid.layers.conv2d(input=data, num_filters=2, filter_size=3, act="relu")\n    '
    if (not isinstance(input, Variable)):
        raise TypeError(("The type of 'input' in conv2d must be Variable, but received %s" % type(input)))
    if (convert_dtype(input.dtype) in ['float16']):
        warnings.warn("The data type of 'input' in conv2d only support float16 on GPU now.")
    if (convert_dtype(input.dtype) not in ['float16', 'float32', 'float64']):
        raise TypeError(("The data type of 'input' in conv2d must be float16 or float32 or float64, but received %s." % convert_dtype(input.dtype)))
    num_channels = input.shape[1]
    if (not isinstance(use_cudnn, bool)):
        raise ValueError(('Attr(use_cudnn) should be True or False. Received Attr(use_cudnn): %s. ' % str(use_cudnn)))
    if (data_format not in ['NCHW', 'NHWC']):
        raise ValueError(("Attr(data_format) should be 'NCHW' or 'NHWC'. Received Attr(data_format): %s." % str(data_format)))
    channel_last = (data_format == 'NHWC')
    num_channels = (input.shape[3] if channel_last else input.shape[1])
    if (num_channels < 0):
        raise ValueError(('The channel dimmention of the input(%s) should be defined. Received: %s.' % (str(input.shape), str(num_channels))))
    assert (param_attr is not False), 'param_attr should not be False here.'
    l_type = 'conv2d'
    if ((num_channels == groups) and ((num_filters % num_channels) == 0) and (not use_cudnn)):
        l_type = 'depthwise_conv2d'
    helper = LayerHelper(l_type, **locals())
    dtype = helper.input_dtype()
    if (groups is None):
        num_filter_channels = num_channels
    else:
        if ((num_channels % groups) != 0):
            raise ValueError('the channel of input must be divisible by groups,received: the channel of input is {}, the shape of input is {}, the groups is {}'.format(num_channels, input.shape, groups))
        num_filter_channels = (num_channels // groups)
    filter_size = utils.convert_to_list(filter_size, 2, 'filter_size')
    stride = utils.convert_to_list(stride, 2, 'stride')
    dilation = utils.convert_to_list(dilation, 2, 'dilation')

    def _update_padding(padding, data_format):

        def is_list_or_tuple(ele):
            if (isinstance(ele, list) or isinstance(ele, tuple)):
                return True
            return False
        if (is_list_or_tuple(padding) and (len(padding) == 4)):
            if (is_list_or_tuple(padding[0]) and (data_format == 'NCHW')):
                if (not ((padding[0] == [0, 0]) and (padding[1] == [0, 0]))):
                    raise ValueError(('Non-zero padding(%s) in the batch or channel dimensions is not supported.' % str(padding)))
                padding = padding[2:4]
                padding = [ele for a_list in padding for ele in a_list]
            elif (is_list_or_tuple(padding[0]) and (data_format == 'NHWC')):
                if (not ((padding[0] == [0, 0]) and (padding[3] == [0, 0]))):
                    raise ValueError(('Non-zero padding(%s) in the batch or channel dimensions is not supported.' % str(padding)))
                padding = padding[1:3]
                padding = [ele for a_list in padding for ele in a_list]
            padding = utils.convert_to_list(padding, 4, 'padding')
        else:
            padding = utils.convert_to_list(padding, 2, 'padding')
            padding = [padding[0], padding[0], padding[1], padding[1]]
        return padding
    padding_algorithm = 'EXPLICIT'
    if isinstance(padding, str):
        padding = padding.upper()
        if (padding not in ['SAME', 'VALID']):
            raise ValueError(("Unknown padding: '%s'. It can only be 'SAME' or 'VALID'." % str(padding)))
        if (padding == 'VALID'):
            padding_algorithm = 'VALID'
            padding = [0, 0, 0, 0]
        elif (padding == 'SAME'):
            padding_algorithm = 'SAME'
            padding = [0, 0, 0, 0]
    padding = _update_padding(padding, data_format)
    filter_shape = ([num_filters, int(num_filter_channels)] + filter_size)

    def _get_default_param_initializer():
        filter_elem_num = ((filter_size[0] * filter_size[1]) * num_channels)
        std = ((2.0 / filter_elem_num) ** 0.5)
        return Normal(0.0, std, 0)
    filter_param = helper.create_parameter(attr=helper.param_attr, shape=filter_shape, dtype=dtype, default_initializer=_get_default_param_initializer())
    pre_bias = helper.create_variable_for_type_inference(dtype)
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
        'use_mkldnn': False,
        'fuse_relu_before_depthwise_conv': False,
        'padding_algorithm': padding_algorithm,
        'data_format': data_format,
    })
    if (data_format == 'NCHW'):
        pre_act = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    else:
        pre_act = helper.append_bias_op(pre_bias, dim_start=3, dim_end=4)
    return helper.append_activation(pre_act)