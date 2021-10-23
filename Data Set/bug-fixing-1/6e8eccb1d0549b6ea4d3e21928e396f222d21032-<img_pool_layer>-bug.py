

@wrap_name_default('pool')
@layer_support()
def img_pool_layer(input, pool_size, name=None, num_channels=None, pool_type=None, stride=1, padding=0, layer_attr=None, pool_size_y=None, stride_y=None, padding_y=None, ceil_mode=True):
    "\n    Image pooling Layer.\n\n    The details of pooling layer, please refer ufldl's pooling_ .\n\n    .. _pooling: http://ufldl.stanford.edu/tutorial/supervised/Pooling/\n\n    - ceil_mode=True:\n\n    ..  math::\n\n        w = 1 + int(ceil(input\\_width + 2 * padding - pool\\_size) / float(stride))\n        h = 1 + int(ceil(input\\_height + 2 * padding\\_y - pool\\_size\\_y) / float(stride\\_y))\n\n    - ceil_mode=False:\n\n    ..  math::\n\n        w = 1 + int(floor(input\\_width + 2 * padding - pool\\_size) / float(stride))\n        h = 1 + int(floor(input\\_height + 2 * padding\\_y - pool\\_size\\_y) / float(stride\\_y))\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        maxpool = img_pool_layer(input=conv,\n                                 pool_size=3,\n                                 pool_size_y=5,\n                                 num_channels=8,\n                                 stride=1,\n                                 stride_y=2,\n                                 padding=1,\n                                 padding_y=2,\n                                 pool_type=MaxPooling())\n\n    :param padding: pooling padding width.\n    :type padding: int\n    :param padding_y: pooling padding height. It's equal to padding by default.\n    :type padding_y: int|None\n    :param name: name of pooling layer\n    :type name: basestring.\n    :param input: layer's input\n    :type input: LayerOutput\n    :param pool_size: pooling window width\n    :type pool_size: int\n    :param pool_size_y: pooling window height. It's eaqual to pool_size by default.\n    :type pool_size_y: int|None\n    :param num_channels: number of input channel.\n    :type num_channels: int\n    :param pool_type: pooling type. MaxPooling or AvgPooling. Default is\n                      MaxPooling.\n    :type pool_type: BasePoolingType\n    :param stride: stride width of pooling.\n    :type stride: int\n    :param stride_y: stride height of pooling. It is equal to stride by default.\n    :type stride_y: int|None\n    :param layer_attr: Extra Layer attribute.\n    :type layer_attr: ExtraLayerAttribute\n    :param ceil_mode: Wether to use ceil mode to calculate output height and with.\n                      Defalut is True. If set false, Otherwise use floor.\n\n    :type ceil_mode: bool\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    "
    if (num_channels is None):
        assert (input.num_filters is not None)
        num_channels = input.num_filters
    assert (type(pool_type) in [AvgPooling, MaxPooling, CudnnAvgPooling, CudnnMaxPooling]), 'only (Cudnn)AvgPooling, (Cudnn)MaxPooling are supported'
    if (pool_type is None):
        pool_type = MaxPooling()
    elif isinstance(pool_type, AvgPooling):
        pool_type.name = 'avg'
    type_name = ((pool_type.name + '-projection') if (isinstance(pool_type, AvgPooling) or isinstance(pool_type, MaxPooling)) else pool_type.name)
    pool_size_y = (pool_size if (pool_size_y is None) else pool_size_y)
    stride_y = (stride if (stride_y is None) else stride_y)
    padding_y = (padding if (padding_y is None) else padding_y)
    l = Layer(name=name, type=LayerType.POOL_LAYER, inputs=[Input(input.name, pool=Pool(pool_type=type_name, channels=num_channels, size_x=pool_size, start=None, stride=stride, padding=padding, size_y=pool_size_y, stride_y=stride_y, padding_y=padding_y))], ceil_mode=ceil_mode, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name, LayerType.POOL_LAYER, parents=[input], num_filters=num_channels, size=l.config.size)
