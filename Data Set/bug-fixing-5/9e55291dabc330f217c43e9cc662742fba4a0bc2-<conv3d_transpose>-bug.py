def conv3d_transpose(input, num_filters, output_size=None, filter_size=None, padding=0, stride=1, dilation=1, groups=None, param_attr=None, bias_attr=None, use_cudnn=True, act=None, name=None, data_format='NCDHW'):
    '\n    The convolution3D transpose layer calculates the output based on the input,\n    filter, and dilations, strides, paddings. Input(Input) and output(Output)\n    are in NCDHW or NDHWC format. Where N is batch size, C is the number of channels,\n    D is the depth of the feature, H is the height of the feature, and W\n    is the width of the feature. Parameters(dilations, strides, paddings) are\n    two elements. These two elements represent height and width, respectively.\n    The details of convolution transpose layer, please refer to the following\n    explanation and references `therein <https://arxiv.org/pdf/1603.07285.pdf>`_.\n    If bias attribution and activation type are provided, bias is added to\n    the output of the convolution, and the corresponding activation function\n    is applied to the final result.\n\n    For each input :math:`X`, the equation is:\n\n    .. math::\n\n        Out = \\sigma (W \\ast X + b)\n\n    In the above equation:\n\n    * :math:`X`: Input value, a Tensor with NCDHW or NDHWC format.\n    * :math:`W`: Filter value, a Tensor with MCDHW format.\n    * :math:`\\ast`: Convolution operation.\n    * :math:`b`: Bias value, a 2-D Tensor with shape [M, 1].\n    * :math:`\\sigma`: Activation function.\n    * :math:`Out`: Output value, the shape of :math:`Out` and :math:`X` may be different.\n\n    Example:\n\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, D_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{in}, C_{out}, D_f, H_f, W_f)`\n\n        - Output:\n\n          Output shape: :math:`(N, C_{out}, D_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n           D^\\prime_{out} &= (D_{in} - 1) * strides[0] - 2 * paddings[0] + dilations[0] * (D_f - 1) + 1 \\\\\n           H^\\prime_{out} &= (H_{in} - 1) * strides[1] - 2 * paddings[1] + dilations[1] * (H_f - 1) + 1 \\\\\n           W^\\prime_{out} &= (W_{in} - 1) * strides[2] - 2 * paddings[2] + dilations[2] * (W_f - 1) + 1 \\\\\n           D_{out} &\\in [ D^\\prime_{out}, D^\\prime_{out} + strides[0] ] \\\\\n           H_{out} &\\in [ H^\\prime_{out}, H^\\prime_{out} + strides[1] ] \\\\\n           W_{out} &\\in [ W^\\prime_{out}, W^\\prime_{out} + strides[2] ]\n\n    Note:\n          The conv3d_transpose can be seen as the backward of the conv3d. For conv3d, \n          when stride > 1, conv3d maps multiple input shape to the same output shape, \n          so for conv3d_transpose, when stride > 1, input shape maps multiple output shape.\n          If output_size is None, :math:`H_{out} = H^\\prime_{out}, :math:`H_{out} =           H^\\prime_{out}, W_{out} = W^\\prime_{out}`; else, the :math:`D_{out}` of the output \n          size must between :math:`D^\\prime_{out}` and :math:`D^\\prime_{out} + strides[0]`, \n          the :math:`H_{out}` of the output size must between :math:`H^\\prime_{out}` \n          and :math:`H^\\prime_{out} + strides[1]`, and the :math:`W_{out}` of the output size must \n          between :math:`W^\\prime_{out}` and :math:`W^\\prime_{out} + strides[2]`, \n          conv3d_transpose can compute the kernel size automatically.\n\n    Args:\n        input(Variable): The input is 5-D Tensor with shape [N, C, D, H, W] or [N, D, H, W, C], the data type \n            of input is float32 or float64.\n        num_filters(int): The number of the filter. It is as same as the output\n            image channel.\n        output_size(int|tuple, optional): The output image size. If output size is a\n            tuple, it must contain three integers, (image_depth, image_height, image_width). This\n            parameter only works when filter_size is None. If output_size and filter_size are \n            specified at the same time, They should follow the formula above. Default: None. \n            Output_size and filter_size should not be None at the same time.\n        filter_size(int|tuple, optional): The filter size. If filter_size is a tuple,\n            it must contain three integers, (filter_size_depth, filter_size_height,\n            filter_size_width). Otherwise, filter_size_depth = filter_size_height =             filter_size_width = filter_size. None if use output size to\n            calculate filter_size. Default: None. filter_size and output_size should not be \n            None at the same time.\n        padding(int|list|str|tuple, optional): The padding size. The padding argument effectively\n             adds `dilation * (kernel - 1)` amount of zero-padding on both sides of input. If `padding` is a string,\n             either \'VALID\' or \'SAME\' supported, which is the padding algorithm. If `padding`\n             is a tuple or list, it could be in three forms: `[pad_depth, pad_height, pad_width]` or\n            `[pad_depth_front, pad_depth_back, pad_height_top, pad_height_bottom, pad_width_left, pad_width_right]`,\n            and when `data_format` is `\'NCDHW\'`, `padding` can be in the form\n            `[[0,0], [0,0], [pad_depth_front, pad_depth_back], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right]]`.\n            when `data_format` is `\'NDHWC\'`, `padding` can be in the form\n            `[[0,0], [pad_depth_front, pad_depth_back], [pad_height_top, pad_height_bottom], [pad_width_left, pad_width_right], [0,0]]`.\n            Default: padding = 0.\n        stride(int|tuple, optional): The stride size. It means the stride in transposed convolution. \n            If stride is a tuple, it must contain three integers, (stride_depth, stride_height, \n            stride_width). Otherwise, stride_depth = stride_height = stride_width = stride. \n            Default: stride = 1.\n        dilation(int|tuple, optional): The dilation size. It means the spacing between the kernel points. \n            If dilation is a tuple, it must contain three integers, (dilation_depth, dilation_height, \n            dilation_width). Otherwise, dilation_depth = dilation_height = dilation_width = dilation. \n            Default: dilation = 1.\n        groups(int, optional): The groups number of the Conv3d transpose layer. Inspired by\n            grouped convolution in Alex Krizhevsky\'s Deep CNN paper, in which\n            when group=2, the first half of the filters is only connected to the\n            first half of the input channels, while the second half of the\n            filters is only connected to the second half of the input channels.\n            Default: groups=1\n        param_attr (ParamAttr, optional): The parameter attribute for learnable parameters/weights\n            of conv3d_transpose. If it is set to None or one attribute of ParamAttr, conv3d_transpose\n            will create ParamAttr as param_attr. If the Initializer of the param_attr\n            is not set, the parameter is initialized with Xavier. Default: None.\n        bias_attr (ParamAttr|bool, optional): The parameter attribute for the bias of conv3d_transpose.\n            If it is set to False, no bias will be added to the output units.\n            If it is set to None or one attribute of ParamAttr, conv3d_transpose\n            will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n            is not set, the bias is initialized zero. Default: None.\n        use_cudnn(bool, optional): Use cudnn kernel or not, it is valid only when the cudnn\n            library is installed. Default: True\n        act (str, optional): Activation type, if it is set to None, activation is not appended.\n            Default: None.\n        name(str, optional): For detailed information, please refer \n           to :ref:`api_guide_Name`. Usually name is no need to set and \n           None by default.\n        data_format(str, optional):The data format of the input and output data. An optional string from: `"NCHW"`, `"NHWC"`.\n            When it is `"NCHW"`, the data is stored in the order of: `[batch_size, input_channels, input_height, input_width]`.\n            Default: \'NCDHW\'.\n\n    Returns:\n        A Variable holding Tensor representing the conv3d_transpose, whose data \n        type is the same with input and shape is (num_batches, channels, out_d, out_h, \n        out_w) or (num_batches, out_d, out_h, out_w, channels). If act is None, the tensor \n        variable storing the transposed convolution result, and if act is not None, the tensor \n        variable storing transposed convolution and non-linearity activation result.\n\n    Raises:\n        ValueError: If the shapes of output, input, filter_size, stride, padding and\n                    groups mismatch.\n\n    Examples:\n       .. code-block:: python\n\n          import paddle.fluid as fluid\n          data = fluid.data(name=\'data\', shape=[None, 3, 12, 32, 32], dtype=\'float32\')\n          conv3d_transpose = fluid.layers.conv3d_transpose(input=data, num_filters=2, filter_size=3)\n    '
    assert (param_attr is not False), 'param_attr should not be False in conv3d_transpose.'
    if (data_format not in ['NCDHW', 'NDHWC']):
        raise ValueError((('Param(data_format) of Op(fluid.layers.conv3d_transpose) got wrong value: received ' + data_format) + ' but only NCDHW or NDHWC supported.'))
    l_type = 'conv3d_transpose'
    helper = LayerHelper(l_type, **locals())
    if (not isinstance(input, Variable)):
        raise TypeError('Input of conv3d_transpose must be Variable')
    input_channel = (input.shape[1] if (data_format == 'NCDHW') else input.shape[(- 1)])
    stride = utils.convert_to_list(stride, 3, 'stride')
    dilation = utils.convert_to_list(dilation, 3, 'dilation')
    if (not isinstance(use_cudnn, bool)):
        raise ValueError('use_cudnn should be True or False')

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
    if (filter_size is None):
        if (output_size is None):
            raise ValueError('output_size must be set when filter_size is None')
        if isinstance(output_size, int):
            output_size = [output_size, output_size]
        d_in = (input.shape[2] if (data_format == 'NCDHW') else input.shape[1])
        h_in = (input.shape[3] if (data_format == 'NCDHW') else input.shape[2])
        w_in = (input.shape[4] if (data_format == 'NCDHW') else input.shape[3])
        filter_size_d = ((((((output_size[0] - ((d_in - 1) * stride[0])) + padding[0]) + padding[1]) - 1) // dilation[0]) + 1)
        filter_size_h = ((((((output_size[1] - ((h_in - 1) * stride[1])) + padding[2]) + padding[3]) - 1) // dilation[1]) + 1)
        filter_size_w = ((((((output_size[2] - ((w_in - 1) * stride[2])) + padding[4]) + padding[5]) - 1) // dilation[2]) + 1)
        filter_size = [filter_size_d, filter_size_h, filter_size_w]
    else:
        filter_size = utils.convert_to_list(filter_size, 3, 'conv3d_transpose.filter_size')
    groups = (1 if (groups is None) else groups)
    filter_shape = ([input_channel, (num_filters // groups)] + filter_size)
    img_filter = helper.create_parameter(dtype=input.dtype, shape=filter_shape, attr=helper.param_attr)
    if (data_format == 'NCDHW'):
        data_format = 'NCHW'
    if (data_format == 'NDHWC'):
        data_format = 'NHWC'
    pre_bias = helper.create_variable_for_type_inference(dtype=input.dtype)
    helper.append_op(type=l_type, inputs={
        'Input': [input],
        'Filter': [img_filter],
    }, outputs={
        'Output': pre_bias,
    }, attrs={
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