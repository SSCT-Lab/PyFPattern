def conv2d_transpose(input, num_filters, output_size=None, filter_size=None, padding=0, stride=1, dilation=1, groups=None, param_attr=None, bias_attr=None, use_cudnn=True, act=None, name=None, data_format='NCHW'):
    '\n    The convolution2D transpose layer calculates the output based on the input,\n    filter, and dilations, strides, paddings. Input(Input) and output(Output)\n    are in NCHW or NHWC format. Where N is batch size, C is the number of channels,\n    H is the height of the feature, and W is the width of the feature.\n    Parameters(dilations, strides, paddings) are two elements. These two elements\n    represent height and width, respectively. The details of convolution transpose\n    layer, please refer to the following explanation and references\n    `therein <https://arxiv.org/pdf/1603.07285.pdf>`_.\n    If bias attribution and activation type are provided, bias is added to\n    the output of the convolution, and the corresponding activation function\n    is applied to the final result.\n\n    For each input :math:`X`, the equation is:\n\n    .. math::\n\n        Out = \\sigma (W \\ast X + b)\n\n    Where:\n\n    * :math:`X`: Input value, a 4-D Tensor with NCHW or NHWC format.\n    * :math:`W`: Filter value, a 4-D Tensor with MCHW format.\n    * :math:`\\ast`: Convolution operation.\n    * :math:`b`: Bias value, a 2-D Tensor with shape [M, 1].\n    * :math:`\\sigma`: Activation function.\n    * :math:`Out`: Output value, a 4-D Tensor with data format \'NCHW\' or \'NHWC\', the shape of :math:`Out` and :math:`X` may be different.\n\n    Example:\n\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{in}, C_{out}, H_f, W_f)`\n\n        - Output:\n\n          Output shape: :math:`(N, C_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n           H^\\prime_{out} &= (H_{in} - 1) * strides[0] - pad_height_top - pad_height_bottom + dilations[0] * (H_f - 1) + 1 \\\\\n           W^\\prime_{out} &= (W_{in} - 1) * strides[1] - pad_width_left - pad_width_right + dilations[1] * (W_f - 1) + 1 \\\\\n           H_{out} &\\in [ H^\\prime_{out}, H^\\prime_{out} + strides[0] ] \\\\\n           W_{out} &\\in [ W^\\prime_{out}, W^\\prime_{out} + strides[1] ]\n\n    Note:\n          The conv2d_transpose can be seen as the backward of the conv2d. For conv2d, \n          when stride > 1, conv2d maps multiple input shape to the same output shape, \n          so for conv2d_transpose, when stride > 1, input shape maps multiple output shape.\n          If output_size is None, :math:`H_{out} = H^\\prime_{out}, W_{out} = W^\\prime_{out}`; \n          else, the :math:`H_{out}` of the output size must between :math:`H^\\prime_{out}` \n          and :math:`H^\\prime_{out} + strides[0]`, and the :math:`W_{out}` of the output size must \n          between :math:`W^\\prime_{out}` and :math:`W^\\prime_{out} + strides[1]`, \n          conv2d_transpose can compute the kernel size automatically.\n\n    Args:\n        input(Variable): 4-D Tensor with [N, C, H, W] or [N, H, W, C] format,\n                         its data type is float32 or float64.\n        num_filters(int): The number of the filter. It is as same as the output\n            image channel.\n        output_size(int|tuple, optional): The output image size. If output size is a\n            tuple, it must contain two integers, (image_height, image_width). None if use\n            filter_size, padding, and stride to calculate output_size.\n            If output_size and filter_size are specified at the same time, They\n            should follow the formula above. Default: None. output_size and filter_size \n            should not be None at the same time.\n        filter_size(int|tuple, optional): The filter size. If filter_size is a tuple,\n            it must contain two integers, (filter_size_height, filter_size_width).\n            Otherwise, filter_size_height = filter_size_width = filter_size. None if \n            use output size to calculate filter_size. Default: None. filter_size and \n            output_size should not be None at the same time.\n        stride(int|tuple, optional): The stride size. It means the stride in transposed convolution. \n            If stride is a tuple, it must contain two integers, (stride_height, stride_width). \n            Otherwise, stride_height = stride_width = stride. Default: stride = 1.\n        padding(int|list|str|tuple, optional): The padding size. The padding argument effectively adds\n             `dilation * (kernel - 1)` amount of zero-padding on both sides of input. If `padding` is a\n             string, either \'VALID\' or \'SAME\' supported, which is the padding algorithm.\n             If `padding` is a tuple or list, it could be in three forms:\n             `[pad_height, pad_width]` or\n            `[pad_height_top, pad_height_bottom, pad_width_left, pad_width_right]`, and\n            when `data_format` is `\'NCHW\'`,\n            `padding` can be in the form `[[0,0], [0,0], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right]]`.\n            when `data_format` is `\'NHWC\'`, `padding` can be in the form\n            `[[0,0], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right], [0,0]]`.\n            Default: padding = 0.\n        dilation(int|tuple, optional): The dilation size. It means the spacing between the kernel points. \n            If dilation is a tuple, it must contain two integers, (dilation_height, dilation_width). \n            Otherwise, dilation_height = dilation_width = dilation. Default: dilation = 1.\n        filter_size(int|tuple, optional): The filter size. If filter_size is a tuple,\n            it must contain two integers, (filter_size_height, filter_size_width).\n            Otherwise, filter_size_height = filter_size_width = filter_size. None if \n            use output size to calculate filter_size. Default: None.\n        groups(int, optional): The groups number of the Conv2d transpose layer. Inspired by\n            grouped convolution in Alex Krizhevsky\'s Deep CNN paper, in which\n            when group=2, the first half of the filters is only connected to the\n            first half of the input channels, while the second half of the\n            filters is only connected to the second half of the input channels.\n            Default: groups = 1.\n        param_attr (ParamAttr, optional): The parameter attribute for learnable parameters/weights\n            of conv2d_transpose. If it is set to None or one attribute of ParamAttr, conv2d_transpose\n            will create ParamAttr as param_attr. If the Initializer of the param_attr\n            is not set, the parameter is initialized with Xavier. Default: None.\n        bias_attr (ParamAttr|bool, optional): The parameter attribute for the bias of conv2d_transpose.\n            If it is set to False, no bias will be added to the output units.\n            If it is set to None or one attribute of ParamAttr, conv2d_transpose\n            will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n            is not set, the bias is initialized zero. Default: None.\n        use_cudnn(bool, optional): Use cudnn kernel or not, it is valid only when the cudnn\n            library is installed. Default: True.\n        act (str, optional): Activation type, if it is set to None, activation is not appended.\n            Default: None.\n        name(str, optional): For detailed information, please refer \n           to :ref:`api_guide_Name`. Usually name is no need to set and \n           None by default.\n        data_format(str, optional): The data format of the input and output data. An optional string\n            from: `"NCHW"`, `"NHWC"`. When it is `"NCHW"`, the data is stored in the order of:\n            `[batch_size, input_channels, input_height, input_width]`. Default: \'NCHW\'.\n\n    Returns:\n        A Variable holding Tensor representing the conv2d_transpose, whose \n        data type is the same with input and shape is (num_batches, channels, out_h, \n        out_w) or (num_batches, out_h, out_w, channels). If act is None, the tensor variable \n        storing the transposed convolution result, and if act is not None, the \n        tensor variable storing transposed convolution and non-linearity activation \n        result.\n\n    Raises:\n        ValueError: If the shapes of output, input, filter_size, stride, padding and\n                    groups mismatch.\n\n    Examples:\n       .. code-block:: python\n\n          import paddle.fluid as fluid\n          data = fluid.data(name=\'data\', shape=[None, 3, 32, 32], dtype=\'float32\')\n          conv2d_transpose = fluid.layers.conv2d_transpose(input=data, num_filters=2, filter_size=3)\n    '
    assert (param_attr is not False), 'param_attr should not be False in conv2d_transpose.'
    if (data_format not in ['NCHW', 'NHWC']):
        raise ValueError((('Attr(data_format) of Op(fluid.layers.conv2d_transpose) got wrong value: received ' + data_format) + ' but only NCHW or NHWC supported.'))
    input_channel = (input.shape[1] if (data_format == 'NCHW') else input.shape[(- 1)])
    op_type = 'conv2d_transpose'
    if ((input_channel == groups) and (num_filters == input_channel) and (not use_cudnn)):
        op_type = 'depthwise_conv2d_transpose'
    helper = LayerHelper(op_type, **locals())
    if (not isinstance(input, Variable)):
        raise TypeError('Input of conv2d_transpose must be Variable')
    stride = utils.convert_to_list(stride, 2, 'stride')
    dilation = utils.convert_to_list(dilation, 2, 'dilation')
    if (not isinstance(use_cudnn, bool)):
        raise ValueError('use_cudnn should be True or False')

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
    if (filter_size is None):
        if (output_size is None):
            raise ValueError('output_size must be set when filter_size is None')
        if isinstance(output_size, int):
            output_size = [output_size, output_size]
        h_in = (input.shape[2] if (data_format == 'NCHW') else input.shape[1])
        w_in = (input.shape[3] if (data_format == 'NCHW') else input.shape[2])
        filter_size_h = ((((((output_size[0] - ((h_in - 1) * stride[0])) + padding[0]) + padding[1]) - 1) // dilation[0]) + 1)
        filter_size_w = ((((((output_size[1] - ((w_in - 1) * stride[1])) + padding[2]) + padding[3]) - 1) // dilation[1]) + 1)
        filter_size = [filter_size_h, filter_size_w]
    else:
        filter_size = utils.convert_to_list(filter_size, 2, 'conv2d_transpose.filter_size')
    if (output_size is None):
        output_size = []
    elif (isinstance(output_size, list) or isinstance(output_size, int)):
        output_size = utils.convert_to_list(output_size, 2, 'output_size')
    else:
        raise ValueError('output_size should be list or int')
    groups = (1 if (groups is None) else groups)
    filter_shape = ([input_channel, (num_filters // groups)] + filter_size)
    img_filter = helper.create_parameter(dtype=input.dtype, shape=filter_shape, attr=helper.param_attr)
    pre_bias = helper.create_variable_for_type_inference(dtype=input.dtype)
    helper.append_op(type=op_type, inputs={
        'Input': [input],
        'Filter': [img_filter],
    }, outputs={
        'Output': pre_bias,
    }, attrs={
        'output_size': output_size,
        'strides': stride,
        'paddings': padding,
        'padding_algorithm': padding_algorithm,
        'dilations': dilation,
        'groups': groups,
        'use_cudnn': use_cudnn,
        'data_format': data_format,
    })
    pre_act = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    out = helper.append_activation(pre_act)
    return out