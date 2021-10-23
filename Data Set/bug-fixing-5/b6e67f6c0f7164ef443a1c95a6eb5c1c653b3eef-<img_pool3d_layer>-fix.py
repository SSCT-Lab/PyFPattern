@wrap_name_default('pool3d')
@layer_support()
def img_pool3d_layer(input, pool_size, name=None, num_channels=None, pool_type=None, stride=1, padding=0, layer_attr=None, pool_size_y=None, stride_y=None, padding_y=None, pool_size_z=None, stride_z=None, padding_z=None, ceil_mode=True):
    "\n    Image pooling Layer.\n\n    The details of pooling layer, please refer ufldl's pooling_ .\n\n    .. _pooling: http://ufldl.stanford.edu/tutorial/supervised/Pooling/\n\n    - ceil_mode=True:\n\n    ..  math::\n\n        w = 1 + \x0crac{ceil(input\\_width + 2 * padding - pool\\_size)}{stride} \\\\\n        h = 1 + \x0crac{ceil(input\\_height + 2 * padding\\_y - pool\\_size\\_y)}{stride\\_y} \\\\\n        d = 1 + \x0crac{ceil(input\\_depth + 2 * padding\\_z - pool\\_size\\_z)}{stride\\_z}\n\n    - ceil_mode=False:\n\n    ..  math::\n\n        w = 1 + \x0crac{floor(input\\_width + 2 * padding - pool\\_size)}{stride} \\\\\n        h = 1 + \x0crac{floor(input\\_height + 2 * padding\\_y - pool\\_size\\_y)}{stride\\_y} \\\\\n        d = 1 + \x0crac{floor(input\\_depth + 2 * padding\\_z - pool\\_size\\_z)}{stride\\_z} \\\\\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        maxpool = img_pool3d_layer(input=conv,\n                                 pool_size=3,\n                                 num_channels=8,\n                                 stride=1,\n                                 padding=1,\n                                 pool_type=MaxPooling())\n\n    :param padding: pooling padding width.\n    :type padding: int | tuple | list\n    :param name: The name of this layer. It is optional.\n    :type name: basestring.\n    :param input: The input of this layer.\n    :type input: LayerOutput\n    :param pool_size: The pooling window lengths along three axises. If the parameter\n                      is set to one integer, the three lengths will be same.\n    :type pool_size: int | tuple | list\n    :param num_channels: The number of input channels. If the parameter is not set or\n                         set to None, its actual value will be automatically set to\n                         the channels number of the input.\n    :type num_channels: int\n    :param pool_type: Pooling type. MaxPooling is the default pooling.\n    :type pool_type: BasePoolingType\n    :param stride: The strides of the pooling along three axises. If the parameter\n                   is set to one integer, the three strides will be same. 1 is the\n                   default value.\n    :type stride: int | tuple | list\n    :param padding: The sizes of padding along three axises. If the parameter is set to\n                    one integer, they will be same. 0 is the default padding size.\n    :type padding: int | tuple | list\n    :param layer_attr: The extra layer attribute. See ExtraLayerAttribute for\n                       details.\n    :type layer_attr: ExtraLayerAttribute\n    :param ceil_mode: Wether to use the ceil function to calculate output height and width.\n                      True is the default. If it is set to False, the floor function will\n                      be used.\n    :type ceil_mode: bool\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    "
    if (num_channels is None):
        assert (input.num_filters is not None)
        num_channels = input.num_filters
    if (pool_type is None):
        pool_type = MaxPooling()
    elif isinstance(pool_type, AvgPooling):
        pool_type.name = 'avg'
    type_name = ((pool_type.name + '-projection') if (isinstance(pool_type, AvgPooling) or isinstance(pool_type, MaxPooling)) else pool_type.name)
    if isinstance(pool_size, collections.Sequence):
        assert (len(pool_size) == 3)
        (pool_size, pool_size_y, pool_size_z) = pool_size
    else:
        pool_size_y = pool_size
        pool_size_z = pool_size
    if isinstance(stride, collections.Sequence):
        assert (len(stride) == 3)
        (stride, stride_y, stride_z) = stride
    else:
        stride_y = stride
        stride_z = stride
    if isinstance(padding, collections.Sequence):
        assert (len(padding) == 3)
        (padding, padding_y, padding_y) = padding
    else:
        padding_y = padding
        padding_z = padding
    l = Layer(name=name, type=LayerType.POOL3D_LAYER, inputs=[Input(input.name, pool=Pool3d(pool_type=type_name, channels=num_channels, size_x=pool_size, start=None, stride=stride, padding=padding, size_y=pool_size_y, stride_y=stride_y, padding_y=padding_y, size_z=pool_size_z, stride_z=stride_z, padding_z=padding_z))], ceil_mode=ceil_mode, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name, LayerType.POOL_LAYER, parents=[input], num_filters=num_channels, size=l.config.size)