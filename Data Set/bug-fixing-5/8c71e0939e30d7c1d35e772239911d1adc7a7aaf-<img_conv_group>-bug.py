@wrap_act_default(param_names=['conv_act'], act=ReluActivation())
@wrap_param_default(param_names=['pool_type'], default_factory=(lambda _: MaxPooling()))
def img_conv_group(input, conv_num_filter, pool_size, num_channels=None, conv_padding=1, conv_filter_size=3, conv_act=None, conv_with_batchnorm=False, conv_batchnorm_drop_rate=0, pool_stride=1, pool_type=None, param_attr=None):
    "\n    Image Convolution Group, Used for vgg net.\n\n    :param conv_batchnorm_drop_rate: if conv_with_batchnorm[i] is true,\n        conv_batchnorm_drop_rate[i] represents the drop rate of each batch norm.\n    :type conv_batchnorm_drop_rate: list\n    :param input: layer's input.\n    :type input: LayerOutput\n    :param conv_num_filter: output channels num.\n    :type conv_num_filter: int\n    :param pool_size: pooling filter size.\n    :type pool_size: int\n    :param num_channels: input channels num.\n    :type num_channels: int\n    :param conv_padding: convolution padding size.\n    :type conv_padding: int\n    :param conv_filter_size: convolution filter size.\n    :type conv_filter_size: int\n    :param conv_act: activation funciton after convolution.\n    :type conv_act: BaseActivation\n    :param conv_with_batchnorm: conv_with_batchnorm[i] represents\n        if there is a batch normalization after each convolution.\n    :type conv_with_batchnorm: list\n    :param pool_stride: pooling stride size.\n    :type pool_stride: int\n    :param pool_type: pooling type.\n    :type pool_type: BasePoolingType\n    :param param_attr: Convolution param attribute.\n        None means default attribute.\n    :type param_attr: ParameterAttribute\n    :return: Layer's output\n    :type: LayerOutput\n    "
    tmp = input
    assert isinstance(tmp, LayerOutput)
    assert (isinstance(conv_num_filter, list) or isinstance(conv_num_filter, tuple))
    for each_num_filter in conv_num_filter:
        assert isinstance(each_num_filter, int)
    assert isinstance(pool_size, int)

    def __extend_list__(obj):
        if (not hasattr(obj, '__len__')):
            return ([obj] * len(conv_num_filter))
        else:
            return obj
    conv_padding = __extend_list__(conv_padding)
    conv_filter_size = __extend_list__(conv_filter_size)
    conv_act = __extend_list__(conv_act)
    conv_with_batchnorm = __extend_list__(conv_with_batchnorm)
    conv_batchnorm_drop_rate = __extend_list__(conv_batchnorm_drop_rate)
    for i in xrange(len(conv_num_filter)):
        extra_kwargs = dict()
        if (num_channels is not None):
            extra_kwargs['num_channels'] = num_channels
            num_channels = None
        if conv_with_batchnorm[i]:
            extra_kwargs['act'] = LinearActivation()
        else:
            extra_kwargs['act'] = conv_act[i]
        tmp = img_conv_layer(input=tmp, padding=conv_padding[i], filter_size=conv_filter_size[i], num_filters=conv_num_filter[i], param_attr=param_attr, **extra_kwargs)
        if conv_with_batchnorm[i]:
            dropout = conv_batchnorm_drop_rate[i]
            if ((dropout == 0) or (abs(dropout) < 1e-05)):
                tmp = batch_norm_layer(input=tmp, act=conv_act[i])
            else:
                tmp = batch_norm_layer(input=tmp, act=conv_act[i], layer_attr=ExtraAttr(drop_rate=dropout))
    return img_pool_layer(input=tmp, stride=pool_stride, pool_size=pool_size, pool_type=pool_type)