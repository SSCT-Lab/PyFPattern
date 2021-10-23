def deformable_conv(input, offset, mask, num_filters, filter_size, stride=1, padding=0, dilation=1, groups=None, deformable_groups=None, im2col_step=None, param_attr=None, bias_attr=None, modulated=True, name=None):
    "\n    **Deformable Convolution op**\n\n    Compute 2-D deformable convolution on 4-D input.\n    Given input image x, output feature map y, the deformable convolution operation can be expressed as follow:\n   \n    \n    Deformable Convolution v2: \n    \n    .. math::\n\n        y(p) = \\sum_{k=1}^{K}{w_k * x(p + p_k + \\Delta p_k) * \\Delta m_k}\n\n    Deformable Convolution v1:\n    \n    .. math::\n\n        y(p) = \\sum_{k=1}^{K}{w_k * x(p + p_k + \\Delta p_k)}\n    \n    Where :math:`\\Delta p_k` and :math:`\\Delta m_k` are the learnable offset and modulation scalar for the k-th location, \n    Which :math:`\\Delta m_k` is one in deformable convolution v1. Please refer to `Deformable ConvNets v2: More Deformable, Better Results\n    <https://arxiv.org/abs/1811.11168v2>`_ and `Deformable Convolutional Networks <https://arxiv.org/abs/1703.06211>`_.\n    \n    Example:\n        - Input:\n\n          Input shape: :math:`(N, C_{in}, H_{in}, W_{in})`\n\n          Filter shape: :math:`(C_{out}, C_{in}, H_f, W_f)`\n\n          Offset shape: :math:`(N, 2 * deformable\\_groups * H_f * H_w, H_{in}, W_{in})`\n\n          Mask shape: :math:`(N, deformable\\_groups * H_f * H_w, H_{in}, W_{in})`\n\n        - Output:\n\n          Output shape: :math:`(N, C_{out}, H_{out}, W_{out})`\n\n        Where\n\n        .. math::\n\n            H_{out}&= \\frac{(H_{in} + 2 * paddings[0] - (dilations[0] * (H_f - 1) + 1))}{strides[0]} + 1 \\\\\n            W_{out}&= \\frac{(W_{in} + 2 * paddings[1] - (dilations[1] * (W_f - 1) + 1))}{strides[1]} + 1\n\n    Args:\n        input (Variable): The input image with [N, C, H, W] format. A Tensor with type\n            float32, float64.\n        offset (Variable): The input coordinate offset of deformable convolution layer.\n            A Tensor with type float32, float64.\n        Mask (Variable, Optional): The input mask of deformable covolution layer.\n            A Tensor with type float32, float64.It should be None when you use\n            deformable_conv_v2.\n        num_filters(int): The number of filter. It is as same as the output\n            image channel.\n        filter_size (int|tuple): The filter size. If filter_size is a tuple,\n            it must contain two integers, (filter_size_H, filter_size_W).\n            Otherwise, the filter will be a square.\n        stride (int|tuple): The stride size. If stride is a tuple, it must\n            contain two integers, (stride_H, stride_W). Otherwise, the\n            stride_H = stride_W = stride. Default: stride = 1.\n        padding (int|tuple): The padding size. If padding is a tuple, it must\n            contain two integers, (padding_H, padding_W). Otherwise, the\n            padding_H = padding_W = padding. Default: padding = 0.\n        dilation (int|tuple): The dilation size. If dilation is a tuple, it must\n            contain two integers, (dilation_H, dilation_W). Otherwise, the\n            dilation_H = dilation_W = dilation. Default: dilation = 1.\n        groups (int): The groups number of the deformable conv layer. According to\n            grouped convolution in Alex Krizhevsky's Deep CNN paper: when group=2,\n            the first half of the filters is only connected to the first half\n            of the input channels, while the second half of the filters is only\n            connected to the second half of the input channels. Default: groups=1.\n        deformable_groups (int): The number of deformable group partitions.\n            Default: deformable_groups = 1.\n        im2col_step (int): Maximum number of images per im2col computation; \n            The total batch size should be divisable by this value or smaller\n            than this value; if you face out of memory problem, you can try\n            to use a smaller value here.\n            Default: im2col_step = 64.\n        param_attr (ParamAttr, Optional): The parameter attribute for learnable parameters/weights\n            of deformable conv. If it is set to None or one attribute of ParamAttr,\n            deformable conv will create ParamAttr as param_attr.\n            If the Initializer of the param_attr is not set, the parameter is\n            initialized with :math:`Normal(0.0, std)`, and the \n            :math:`std` is :math:`(\\frac{2.0 }{filter\\_elem\\_num})^{0.5}`. Default: None.\n        bias_attr (ParamAttr|bool, Optional): The parameter attribute for the bias of\n            deformable conv layer. If it is set to False, no bias will be added\n            to the output units. If it is set to None or one attribute of ParamAttr, conv2d\n            will create ParamAttr as bias_attr. If the Initializer of the bias_attr\n            is not set, the bias is initialized zero. Default: None.\n        modulated (bool): Make sure which version should be used between v1 and v2, where v2 is             used while True. Default: True.\n        name(str, Optional): For details, please refer to :ref:`api_guide_Name`.\n                        Generally, no setting is required. Default: None.\n    Returns:\n        Variable: The tensor variable storing the deformable convolution                   result. A Tensor with type float32, float64.\n    Raises:\n        ValueError: If the shapes of input, filter_size, stride, padding and\n                    groups mismatch.\n    Examples:\n        .. code-block:: python\n\n          #deformable conv v2:\n         \n          import paddle.fluid as fluid\n          C_in, H_in, W_in = 3, 32, 32\n          filter_size, deformable_groups = 3, 1\n          data = fluid.data(name='data', shape=[None, C_in, H_in, W_in], dtype='float32')\n          offset = fluid.data(name='offset', shape=[None, 2*deformable_groups*filter_size**2, H_in, W_in], dtype='float32')\n          mask = fluid.data(name='mask', shape=[None, deformable_groups*filter_size**2, H_in, W_in], dtype='float32')\n          out = fluid.layers.deformable_conv(input=data, offset=offset, mask=mask,\n                                             num_filters=2, filter_size=filter_size, padding=1, modulated=True)\n\n          #deformable conv v1:\n\n          import paddle.fluid as fluid\n          C_in, H_in, W_in = 3, 32, 32\n          filter_size, deformable_groups = 3, 1\n          data = fluid.data(name='data', shape=[None, C_in, H_in, W_in], dtype='float32')\n          offset = fluid.data(name='offset', shape=[None, 2*deformable_groups*filter_size**2, H_in, W_in], dtype='float32')\n          out = fluid.layers.deformable_conv(input=data, offset=offset, mask=None,\n                                             num_filters=2, filter_size=filter_size, padding=1, modulated=False)\n    "
    num_channels = input.shape[1]
    assert (param_attr is not False), 'param_attr should not be False here.'
    helper = LayerHelper('deformable_conv', **locals())
    dtype = helper.input_dtype()
    if (not isinstance(input, Variable)):
        raise TypeError('Input of deformable_conv must be Variable')
    if (not isinstance(offset, Variable)):
        raise TypeError('Input Offset of deformable_conv must be Variable')
    if (groups is None):
        num_filter_channels = num_channels
    else:
        if ((num_channels % groups) != 0):
            raise ValueError('num_channels must be divisible by groups.')
        num_filter_channels = (num_channels // groups)
    filter_size = utils.convert_to_list(filter_size, 2, 'filter_size')
    stride = utils.convert_to_list(stride, 2, 'stride')
    padding = utils.convert_to_list(padding, 2, 'padding')
    dilation = utils.convert_to_list(dilation, 2, 'dilation')
    input_shape = input.shape
    filter_shape = ([num_filters, int(num_filter_channels)] + filter_size)

    def _get_default_param_initializer():
        filter_elem_num = ((filter_size[0] * filter_size[1]) * num_channels)
        std = ((2.0 / filter_elem_num) ** 0.5)
        return Normal(0.0, std, 0)
    filter_param = helper.create_parameter(attr=helper.param_attr, shape=filter_shape, dtype=dtype, default_initializer=_get_default_param_initializer())
    pre_bias = helper.create_variable_for_type_inference(dtype)
    if modulated:
        helper.append_op(type='deformable_conv', inputs={
            'Input': input,
            'Filter': filter_param,
            'Offset': offset,
            'Mask': mask,
        }, outputs={
            'Output': pre_bias,
        }, attrs={
            'strides': stride,
            'paddings': padding,
            'dilations': dilation,
            'groups': groups,
            'deformable_groups': deformable_groups,
            'im2col_step': im2col_step,
        })
    else:
        helper.append_op(type='deformable_conv_v1', inputs={
            'Input': input,
            'Filter': filter_param,
            'Offset': offset,
        }, outputs={
            'Output': pre_bias,
        }, attrs={
            'strides': stride,
            'paddings': padding,
            'dilations': dilation,
            'groups': groups,
            'deformable_groups': deformable_groups,
            'im2col_step': im2col_step,
        })
    output = helper.append_bias_op(pre_bias, dim_start=1, dim_end=2)
    return output