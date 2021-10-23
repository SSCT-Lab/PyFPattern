@wrap_name_default('conv3d')
@wrap_param_attr_default()
@wrap_bias_attr_default()
@wrap_act_default(act=ReluActivation())
@layer_support(DROPOUT)
def img_conv3d_layer(input, filter_size, num_filters, name=None, num_channels=None, act=None, groups=1, stride=1, padding=0, bias_attr=None, param_attr=None, shared_biases=True, layer_attr=None, trans=False, layer_type=None):
    '\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        conv = img_conv3d_layer(input=data, filter_size=1,\n                              num_channels=8,\n                              num_filters=16, stride=1,\n                              bias_attr=False,\n                              act=ReluActivation())\n\n    :param name: The name of this layer. It is optional.\n    :type name: basestring\n    :param input: The input of this layer.\n    :type input: LayerOutput\n    :param filter_size: The dimensions of the filter kernel along three axises. If the parameter\n                        is set to one integer, the three dimensions will be same.\n    :type filter_size: int | tuple | list\n    :param num_filters: The number of filters. It is as same as the output image channel.\n    :type num_filters: int\n    :param act: Activation type. ReluActivation is the default activation.\n    :type act: BaseActivation\n    :param groups: The number of the filter groups.\n    :type groups: int\n    :param stride: The strides of the convolution along three axises. If the parameter\n                   is set to one integer, the three strides will be same.\n    :type stride: int | tuple | list\n    :param padding: The numbers of padding along three axises. If the parameter is set to\n                    one integer, they will be same.\n    :type padding: int | tuple | list\n    :param bias_attr: The bias attribute. If the parameter is set to False or an object\n                      whose type is not ParameterAttribute, no bias is defined. If the\n                      parameter is set to True, the bias is initialized to zero.\n    :type bias_attr: ParameterAttribute | None | bool | Any\n    :param num_channels: The number of input channels. If the parameter is not set or\n                         set to None, its actual value will be automatically set to\n                         the channels number of the input.\n    :type num_channels: int\n    :param param_attr: The parameter attribute of the convolution. See ParameterAttribute for\n                       details.\n    :type param_attr: ParameterAttribute\n    :param shared_biases: Whether biases will be shared between filters or not.\n    :type shared_biases: bool\n    :param layer_attr: The extra layer attributes. See ExtraLayerAttribute for\n                       details.\n    :type layer_attr: ExtraLayerAttribute\n    :param trans: True if it is a convTransLayer, False if it is a convLayer\n    :type trans: bool\n    :param layer_type: Specify the layer type. If the parameter is set, it must be "deconv3d"\n                       when trans=True. If not set, it will be automatically set to "deconv3d"\n                       when trans=True and "conv3d" when trans=False.\n    :type layer_type: basestring\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    '
    if (num_channels is None):
        assert (input.num_filters is not None)
        num_channels = input.num_filters
    if isinstance(filter_size, collections.Sequence):
        assert (len(filter_size) == 3)
        (filter_size, filter_size_y, filter_size_z) = filter_size
    else:
        filter_size_y = filter_size
        filter_size_z = filter_size
    if isinstance(stride, collections.Sequence):
        assert (len(stride) == 3)
        (stride, stride_y, stride_z) = stride
    else:
        stride_y = stride
        stride_z = stride
    if isinstance(padding, collections.Sequence):
        assert (len(padding) == 3)
        (padding, padding_y, padding_z) = padding
    else:
        padding_y = padding
        padding_z = padding
    if param_attr.attr.get('initial_smart'):
        init_w = ((2.0 / ((filter_size ** 2) * num_channels)) ** 0.5)
        param_attr.attr['initial_mean'] = 0.0
        param_attr.attr['initial_std'] = init_w
        param_attr.attr['initial_strategy'] = 0
        param_attr.attr['initial_smart'] = False
    if layer_type:
        if trans:
            assert (layer_type in ['deconv3d'])
        lt = layer_type
    else:
        lt = (LayerType.DECONV3D_LAYER if trans else LayerType.CONV3D_LAYER)
    l = Layer(name=name, inputs=Input(input.name, conv=Conv3D(filter_size=filter_size, padding=padding, stride=stride, channels=num_channels, groups=groups, filter_size_y=filter_size_y, padding_y=padding_y, stride_y=stride_y, filter_size_z=filter_size_z, padding_z=padding_z, stride_z=stride_z), **param_attr.attr), active_type=act.name, num_filters=num_filters, bias=ParamAttr.to_bias(bias_attr), shared_biases=shared_biases, type=lt, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name, lt, parents=[input], activation=act, num_filters=num_filters, size=l.config.size)