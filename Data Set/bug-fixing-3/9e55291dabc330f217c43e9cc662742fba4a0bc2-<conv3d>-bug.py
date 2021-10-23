def conv3d(input, num_filters, filter_size, stride=1, padding=0, dilation=1, groups=None, param_attr=None, bias_attr=None, use_cudnn=True, act=None, name=None, data_format='NCDHW'):
    '\n    The convolution3D layer calculates the output based on the input, filter\n    and strides, paddings, dilations, groups parameters. Input(Input) and\n    Output(Output) are in NCDHW or NDHWC format. Where N is batch size C is the number of\n    channels, D is the depth of the feature, H is the height of the feature,\n    and W is the width of the feature. Convlution3D is similar with Convlution2D\n    but adds one dimension(depth). If bias attribution and activation type are\n    provided, bias is added to the output of the convolution, and the\n    corresponding activation function is applied to the final result.\n\n    For each input :math:`X`, the equation is:\n\n    .. math::\n\n        Out = \\sigma (W \\ast X + b)\n\n    In the above equation:\n\n    * :math:`X`: Input value, a tensor with NCDHW or NDHWC format.\n    * :math:`W`: Filter value, a tensor with MCDHW format.\n    * :math:`\\ast`: Convolution operation.\n    * :math:`b`: Bias value, a 2-D tensor with shape [M, 1].\n    * :math:`\\sigma`: Activation function.\n    * :math:`Out`: Output value, the shape of :math:`Out` and :math:`X` may be different.\n\n    Example:\n\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, D_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{out}, C_{in}, D_f, H_f, W_f)`\n\n        - Output:\n          Output shape: :math:`(N, C_{out}, D_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n            D_{out}&= \\frac{(D_{in} + 2 * paddings[0] - (dilations[0] * (D_f - 1) + 1))}{strides[0]} + 1 \\\\\n            H_{out}&= \\frac{(H_{in} + 2 * paddings[1] - (dilations[1] * (H_f - 1) + 1))}{strides[1]} + 1 \\\\\n            W_{out}&= \\frac{(W_{in} + 2 * paddings[2] - (dilations[2] * (W_f - 1) + 1))}{strides[2]} + 1\n\n    Args:\n        input (Variable): The input is 5-D Tensor with shape [N, C, D, H, W], the data \n            type of input is float16 or float32 or float64.\n        num_filters(int): The number of filter. It is as same as the output\n            image channel.\n        filter_size (int|tuple): The filter size. If filter_size is a tuple,\n            it must contain three integers, (filter_size_depth, filter_size_height, \n            filter_size_width). Otherwise, filter_size_depth = filter_size_height =             filter_size_width = filter_size.\n        stride (int|tuple): The stride size. It means the stride in convolution. If stride is a \n            tuple, it must contain three integers, (stride_depth, stride_height, stride_width). \n            Otherwise, stride_depth = stride_height = stride_width = stride. Default: stride = 1.\n        padding (string|int|list|tuple): The padding size. It means the number of zero-paddings \n            on both sides for each dimention. If `padding` is a string, either \'VALID\' or\n            \'SAME\' which is the padding algorithm. If padding size is a tuple or list,\n            it could be in three forms: `[pad_depth, pad_height, pad_width]` or\n            `[pad_depth_front, pad_depth_back, pad_height_top, pad_height_bottom, pad_width_left, pad_width_right]`,\n            and when `data_format` is `"NCDHW"`, `pool_padding` can be in the form\n            `[[0,0], [0,0], [pad_depth_front, pad_depth_back], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right]]`.\n            when `data_format` is `"NDHWC"`, `pool_padding` can be in the form\n            `[[0,0], [pad_depth_front, pad_depth_back], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right], [0,0]]`.\n            Default: padding = 0.\n        dilation (int|tuple): The dilation size. It means the spacing between the kernel points. \n            If dilation is a tuple, it must contain three integers, (dilation_depth, dilation_height,\n            dilation_width). Otherwise, dilation_depth = dilation_height = dilation_width = dilation. \n            Default: dilation = 1.\n        groups (int): The groups number of the Conv3d Layer. According to grouped\n            convolution in Alex Krizhevsky\'s Deep CNN paper: when group=2,\n            the first half of the filters is only connected to the first half\n            of the input channels, while the second half of the filters is only\n            connected to the second half of the input channels. Default: groups=1\n        param_attr (ParamAttr|None): The parameter attribute for learnable parameters/weights\n            of conv3d. If it is set to None or one attribute of ParamAttr, conv3d\n            will create ParamAttr as param_attr. If it is set to None, the parameter\n            is initialized with :math:`Normal(0.0, std)`, and the :math:`std` is\n            :math:`(\\frac{2.0 }{filter\\_elem\\_num})^{0.5}`. Default: None.\n        bias_attr (ParamAttr|bool|None): The parameter attribute for the bias of conv3d.\n            If it is set to False, no bias will be added to the output units.\n            If it is set to None or one attribute of ParamAttr, conv3d\n            will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n            is not set, the bias is initialized zero. Default: None.\n        use_cudnn (bool): Use cudnn kernel or not, it is valid only when the cudnn\n            library is installed. Default: True\n        act (str): Activation type, if it is set to None, activation is not appended.\n            Default: None.\n        name(str|None): For detailed information, please refer \n           to :ref:`api_guide_Name`. Usually name is no need to set and \n           None by default.\n        data_format (str): The data format of the input and output data. An optional string from: `"NCDHW"`, `"NDHWC"`.\n            The default is `"NCDHW"`. When it is `"NCDHW"`, the data is stored in the order of:\n            `[batch_size, input_channels, input_depth, input_height, input_width]`.\n\n    Returns:\n        A Variable holding Tensor representing the conv3d, whose data type is \n        the same with input. If act is None, the tensor variable storing the \n        convolution result, and if act is not None, the tensor variable storing \n        convolution and non-linearity activation result.\n\n    Examples:\n        .. code-block:: python\n\n          import paddle.fluid as fluid\n          data = fluid.data(name=\'data\', shape=[None, 3, 12, 32, 32], dtype=\'float32\')\n          conv3d = fluid.layers.conv3d(input=data, num_filters=2, filter_size=3, act="relu")\n    '
    l_type = 'conv3d'
    assert (param_attr is not False), 'param_attr should not be False here.'
    helper = LayerHelper(l_type, **locals())
    dtype = helper.input_dtype()
    if (not isinstance(use_cudnn, bool)):
        raise ValueError(('Attr(use_cudnn) should be True or False. Received Attr(use_cudnn): %s. ' % str(use_cudnn)))
    if (data_format not in ['NCDHW', 'NDHWC']):
        raise ValueError(("Attr(data_format) should be 'NCDHW' or 'NDHWC'. Received Attr(data_format): %s." % str(data_format)))
    channel_last = (data_format == 'NDHWC')
    num_channels = (input.shape[4] if channel_last else input.shape[1])
    if (num_channels < 0):
        raise ValueError(('The channel dimmention of the input(%s) should be defined. Received: %s.' % (str(input.shape), str(num_channels))))
    if (groups is None):
        num_filter_channels = num_channels
    else:
        if ((num_channels % groups) != 0):
            raise ValueError(('The number of input channels must be divisible by Attr(groups). Received: number of channels(%s), groups(%s).' % (str(num_channels), str(groups))))
        num_filter_channels = (num_channels // groups)
    filter_size = utils.convert_to_list(filter_size, 3, 'filter_size')
    stride = utils.convert_to_list(stride, 3, 'stride')
    dilation = utils.convert_to_list(dilation, 3, 'dilation')

    def _update_padding(padding, data_format):

        def is_list_or_tuple(ele):
            if (isinstance(ele, list) or isinstance(ele, tuple)):
                return True
            return False
        if (is_list_or_tuple(padding) and (len(padding) == 5)):
            if (is_list_or_tuple(padding[0]) and (data_format == 'NCDHW')):
                if (not ((padding[0] == [0, 0]) and (padding[1] == [0, 0]))):
                    raise ValueError(('Non-zero padding(%s) in the batch or channel dimensions is not supported.' % str(padding)))
                padding = padding[2:5]
                padding = [ele for a_list in padding for ele in a_list]
            elif (is_list_or_tuple(padding[0]) and (data_format == 'NDHWC')):
                if (not ((padding[0] == [0, 0]) and (padding[4] == [0, 0]))):
                    raise ValueError(('Non-zero padding(%s) in the batch or channel dimensions is not supported.' % str(padding)))
                padding = padding[1:4]
                padding = [ele for a_list in padding for ele in a_list]
            padding = utils.convert_to_list(padding, 6, 'padding')
        elif (is_list_or_tuple(padding) and (len(padding) == 6)):
            padding = utils.convert_to_list(padding, 6, 'padding')
        else:
            padding = utils.convert_to_list(padding, 3, 'padding')
            padding = [padding[0], padding[0], padding[1], padding[1], padding[2], padding[2]]
        return padding
    padding_algorithm = 'EXPLICIT'
    if isinstance(padding, str):
        padding = padding.upper()
        if (padding not in ['SAME', 'VALID']):
            raise ValueError(("Unknown padding: '%s'. It can only be 'SAME' or 'VALID'." % str(padding)))
        if (padding == 'VALID'):
            padding_algorithm = 'VALID'
            padding = [0, 0, 0, 0, 0, 0]
        elif (padding == 'SAME'):
            padding_algorithm = 'SAME'
            padding = [0, 0, 0, 0, 0, 0]
    padding = _update_padding(padding, data_format)
    input_shape = input.shape
    filter_shape = ([num_filters, num_filter_channels] + filter_size)

    def _get_default_param_initializer():
        filter_elem_num = (((filter_size[0] * filter_size[1]) * filter_size[2]) * num_channels)
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
        'padding_algorithm': padding_algorithm,
        'data_format': data_format,
    })
    pre_act = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    return helper.append_activation(pre_act)