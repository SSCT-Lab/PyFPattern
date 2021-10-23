

@wrap_name_default('pool')
@layer_support()
def img_pool_layer(input, pool_size, name=None, num_channels=None, pool_type=None, stride=1, padding=0, layer_attr=None, pool_size_y=None, stride_y=None, padding_y=None, ceil_mode=True, exclude_mode=None):
    "\n    Image pooling Layer.\n\n    The details of pooling layer, please refer to ufldl's pooling_ .\n\n    .. _pooling: http://ufldl.stanford.edu/tutorial/supervised/Pooling/\n\n    - ceil_mode=True:\n\n    ..  math::\n\n        w & = 1 + ceil(\\frac{input\\_width + 2 * padding - pool\\_size}{stride})\n\n        h & = 1 + ceil(\\frac{input\\_height + 2 * padding\\_y - pool\\_size\\_y}{stride\\_y})\n\n    - ceil_mode=False:\n\n    ..  math::\n\n        w & = 1 + floor(\\frac{input\\_width + 2 * padding - pool\\_size}{stride})\n\n        h & = 1 + floor(\\frac{input\\_height + 2 * padding\\_y - pool\\_size\\_y}{stride\\_y})\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        maxpool = img_pool_layer(input=conv,\n                                 pool_size=3,\n                                 pool_size_y=5,\n                                 num_channels=8,\n                                 stride=1,\n                                 stride_y=2,\n                                 padding=1,\n                                 padding_y=2,\n                                 pool_type=MaxPooling())\n\n    :param padding: The padding size on the x axis. 0 is the default padding size.\n    :type padding: int\n    :param padding_y: The padding size on the y axis. If the parameter is not set\n                      or set to None, it will be set to 'padding' automatically.\n    :param name: The name of this layer. It is optional.\n    :type name: basestring\n    :param input: The input of this layer.\n    :type input: LayerOutput\n    :param pool_size: The pooling window length on the x axis.\n    :type pool_size: int\n    :param pool_size_y: The pooling window length on the y axis. If the parameter is\n                        not set or set to None, its actual value will be automatically\n                        set to pool_size.\n    :type pool_size_y: int\n    :param num_channels: The number of input channels. If the parameter is not set or\n                         set to None, its actual value will be automatically set to\n                         the channels number of the input.\n    :type num_channels: int\n    :param pool_type: Pooling type. MaxPooling is the default pooling.\n    :type pool_type: BasePoolingType\n    :param stride: The stride on the x axis. 1 is the default value.\n    :type stride: int\n    :param stride_y: The stride on the y axis. If the parameter is not set or set to\n                     None, its actual value will be automatically set to 'stride'.\n    :type stride_y: int\n    :param layer_attr: The extra layer attribute. See ExtraLayerAttribute for\n                       details.\n    :type layer_attr: ExtraLayerAttribute\n    :param ceil_mode: Whether to use the ceil function to calculate output height and width.\n                      True is the default. If it is set to False, the floor function will\n                      be used.\n    :type ceil_mode: bool\n    :param exclude_mode: Whether to exclude the padding cells when calculating, but only \n                         work when pool_type is AvgPooling. If None, also exclude the padding \n                         cells. If use cudnn, use CudnnAvgPooling or CudnnAvgInclPadPooling \n                         as pool_type to identify the mode.\n    :type exclude_mode: bool\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    "
    if (num_channels is None):
        assert (input.num_filters is not None)
        num_channels = input.num_filters
    if (pool_type is None):
        pool_type = MaxPooling()
    elif isinstance(pool_type, AvgPooling):
        pool_type.name = 'avg'
    assert (type(pool_type) in [AvgPooling, MaxPooling, MaxWithMaskPooling, CudnnAvgPooling, CudnnMaxPooling, CudnnAvgInclPadPooling]), 'only (Cudnn)AvgPooling, (Cudnn)MaxPooling, MaxWithMaskPooling are supported'
    type_name = ((pool_type.name + '-projection') if (isinstance(pool_type, AvgPooling) or isinstance(pool_type, MaxPooling)) else pool_type.name)
    pool_size_y = (pool_size if (pool_size_y is None) else pool_size_y)
    stride_y = (stride if (stride_y is None) else stride_y)
    padding_y = (padding if (padding_y is None) else padding_y)
    l = Layer(name=name, type=LayerType.POOL_LAYER, inputs=[Input(input.name, pool=Pool(pool_type=type_name, channels=num_channels, size_x=pool_size, start=None, stride=stride, padding=padding, size_y=pool_size_y, stride_y=stride_y, padding_y=padding_y))], ceil_mode=ceil_mode, exclude_mode=exclude_mode, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name, LayerType.POOL_LAYER, parents=[input], num_filters=num_channels, size=l.config.size)
