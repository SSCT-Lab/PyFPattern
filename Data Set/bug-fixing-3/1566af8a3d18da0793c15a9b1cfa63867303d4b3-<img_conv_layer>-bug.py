@wrap_name_default('conv')
@wrap_param_attr_default()
@wrap_bias_attr_default()
@wrap_act_default(act=ReluActivation())
@layer_support(DROPOUT)
def img_conv_layer(input, filter_size, num_filters, name=None, num_channels=None, act=None, groups=1, stride=1, padding=0, dilation=1, bias_attr=None, param_attr=None, shared_biases=True, layer_attr=None, filter_size_y=None, stride_y=None, padding_y=None, dilation_y=None, trans=False, layer_type=None):
    '\n    Convolution layer for image. Paddle can support both square and non-square\n    input currently.\n\n    The details of convolution layer, please refer UFLDL\'s `convolution\n    <http://ufldl.stanford.edu/tutorial/supervised/\n    FeatureExtractionUsingConvolution/>`_ .\n\n    Convolution Transpose (deconv) layer for image. Paddle can support both square\n    and non-square input currently.\n\n    The details of convolution transpose layer,\n    please refer to the following explanation and references therein\n    <http://datascience.stackexchange.com/questions/6107/\n    what-are-deconvolutional-layers/>`_ .\n    The num_channel means input image\'s channel number. It may be 1 or 3 when\n    input is raw pixels of image(mono or RGB), or it may be the previous layer\'s\n    num_filters * num_group.\n\n    There are several groups of filters in PaddlePaddle implementation.\n    Each group will process some channels of the input. For example, if\n    num_channel = 256, group = 4, num_filter=32, the PaddlePaddle will create\n    32*4 = 128 filters to process the input. The channels will be split into 4\n    pieces. First 256/4 = 64 channels will be processed by first 32 filters. The\n    rest channels will be processed by the rest groups of filters.\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        conv = img_conv_layer(input=data, filter_size=1, filter_size_y=1,\n                              num_channels=8,\n                              num_filters=16, stride=1,\n                              bias_attr=False,\n                              act=ReluActivation())\n\n    :param name: The name of this layer. It is optional.\n    :type name: basestring\n    :param input: The input of this layer.\n    :type input: LayerOutput\n    :param filter_size: The dimensions of the filter kernel. If the parameter is\n                        set to one integer, the two dimensions on x and y axises\n                        will be same when filter_size_y is not set. If it is set\n                        to a list, the first element indicates the dimension on\n                        the x axis, and the second is used to specify the dimension\n                        on the y axis when filter_size_y is not provided.\n    :type filter_size: int | tuple | list\n    :param filter_size_y: The dimension of the filter kernel on the y axis. If the parameter\n                          is not set, it will be set automatically according to filter_size.\n    :type filter_size_y: int\n    :param num_filters: Each filter group\'s number of filter\n    :param act: Activation type. ReluActivation is the default activation.\n    :type act: BaseActivation\n    :param groups: The group number. 1 is the default group number.\n    :type groups: int\n    :param stride: The strides. If the parameter is set to one integer, the strides\n                   on x and y axises will be same when stride_y is not set. If it is\n                   set to a list, the first element indicates the stride on the x axis,\n                   and the second is used to specify the stride on the y axis when\n                   stride_y is not provided. 1 is the default value.\n    :type stride: int | tuple | list\n    :param stride_y: The stride on the y axis.\n    :type stride_y: int\n    :param padding: The padding sizes. If the parameter is set to one integer, the padding\n                    sizes on x and y axises will be same when padding_y is not set. If it\n                    is set to a list, the first element indicates the padding size on the\n                    x axis, and the second is used to specify the padding size on the y axis\n                    when padding_y is not provided. 0 is the default padding size.\n    :type padding: int | tuple | list\n    :param padding_y: The padding size on the y axis.\n    :type padding_y: int\n    :param dilation: The dimensions of the dilation. If the parameter is set to one integer,\n                     the two dimensions on x and y axises will be same when dilation_y is not\n                     set. If it is set to a list, the first element indicates the dimension\n                     on the x axis, and the second is used to specify the dimension on the y\n                     axis when dilation_y is not provided. 1 is the default dimension.\n    :type dilation: int | tuple | list\n    :param dilation_y: The dimension of the dilation on the y axis.\n    :type dilation_y: int\n    :param bias_attr: The bias attribute. If the parameter is set to False or an object\n                      whose type is not ParameterAttribute, no bias is defined. If the\n                      parameter is set to True, the bias is initialized to zero.\n    :type bias_attr: ParameterAttribute | None | bool | Any\n    :param num_channels: The number of input channels. If the parameter is not set or\n                         set to None, its actual value will be automatically set to\n                         the channel number of the input.\n    :type num_channels: int\n    :param param_attr: The parameter attribute. See ParameterAttribute for\n                       details.\n    :type param_attr: ParameterAttribute\n    :param shared_biases: Whether biases will be shared between filters or not.\n    :type shared_biases: bool\n    :param layer_attr: The extra layer attributes. See ExtraLayerAttribute for\n                       details.\n    :type layer_attr: ExtraLayerAttribute\n    :param trans: True if it is a convTransLayer, False if it is a convLayer\n    :type trans: bool\n    :param layer_type: Specify the layer type. If the dilation\'s dimension on one axis is\n                       larger than 1, layer_type has to be "cudnn_conv" or "cudnn_convt".\n                       If trans=True, layer_type has to be "exconvt" or "cudnn_convt",\n                       otherwise layer_type has to be either "exconv" or "cudnn_conv".\n    :type layer_type: basestring\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    '
    if (num_channels is None):
        assert (input.num_filters is not None)
        num_channels = input.num_filters
    if (filter_size_y is None):
        if isinstance(filter_size, collections.Sequence):
            assert (len(filter_size) == 2)
            (filter_size, filter_size_y) = filter_size
        else:
            filter_size_y = filter_size
    if (stride_y is None):
        if isinstance(stride, collections.Sequence):
            assert (len(stride) == 2)
            (stride, stride_y) = stride
        else:
            stride_y = stride
    if (padding_y is None):
        if isinstance(padding, collections.Sequence):
            assert (len(padding) == 2)
            (padding, padding_y) = padding
        else:
            padding_y = padding
    if (dilation_y is None):
        if isinstance(dilation, collections.Sequence):
            assert (len(dilation) == 2)
            (dilation, dilation_y) = dilation
        else:
            dilation_y = dilation
    if param_attr.attr.get('initial_smart'):
        init_w = ((2.0 / ((filter_size ** 2) * num_channels)) ** 0.5)
        param_attr.attr['initial_mean'] = 0.0
        param_attr.attr['initial_std'] = init_w
        param_attr.attr['initial_strategy'] = 0
        param_attr.attr['initial_smart'] = False
    if layer_type:
        if ((dilation > 1) or (dilation_y > 1)):
            assert (layer_type in ['cudnn_conv', 'cudnn_convt', 'exconv', 'exconvt'])
        if trans:
            assert (layer_type in ['exconvt', 'cudnn_convt'])
        else:
            assert (layer_type in ['exconv', 'cudnn_conv'])
        lt = layer_type
    else:
        lt = (LayerType.CONVTRANS_LAYER if trans else LayerType.CONV_LAYER)
    l = Layer(name=name, inputs=Input(input.name, conv=Conv(filter_size=filter_size, padding=padding, dilation=dilation, stride=stride, channels=num_channels, groups=groups, filter_size_y=filter_size_y, padding_y=padding_y, dilation_y=dilation_y, stride_y=stride_y), **param_attr.attr), active_type=act.name, num_filters=num_filters, bias=ParamAttr.to_bias(bias_attr), shared_biases=shared_biases, type=lt, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name, lt, parents=[input], activation=act, num_filters=num_filters, size=l.config.size)