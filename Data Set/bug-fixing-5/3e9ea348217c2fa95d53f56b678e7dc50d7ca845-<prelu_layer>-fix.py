@layer_support()
@wrap_name_default()
def prelu_layer(input, name=None, partial_sum=1, channel_shared=None, num_channels=None, param_attr=None, layer_attr=None):
    '\n    The Parametric Relu activation that actives outputs with a learnable weight.\n\n    Reference:\n        Delving Deep into Rectifiers: Surpassing Human-Level Performance on\n        ImageNet Classification http://arxiv.org/pdf/1502.01852v1.pdf\n\n    .. math::\n       z_i &\\quad if \\quad z_i > 0 \\\\\n       a_i * z_i  &\\quad \\mathrm{otherwise}\n\n    The example usage is:\n\n    .. code-block:: python\n\n       prelu = prelu_layer(input=layers, partial_sum=1)\n\n    :param name: The name of this layer. It is optional.\n    :type name: basestring\n    :param input: The input of this layer.\n    :type input: LayerOutput\n    :param partial_sum: this parameter makes a group of inputs share the same weight.\n\n        - partial_sum = 1, indicates the element-wise activation: each element has a weight.\n        - partial_sum = number of elements in one channel, indicates the channel-wise activation, elements in a channel share the same weight.\n        - partial_sum = number of outputs, indicates all elements share the same weight.\n\n    :type partial_sum: int\n    :param channel_shared: whether or not the parameter are shared across channels.\n\n        - channel_shared = True, we set the partial_sum to the number of outputs.\n        - channel_shared = False, we set the partial_sum to the number of elements in one channel.\n\n    :type channel_shared: bool\n    :param num_channels: number of input channel.\n    :type num_channels: int\n    :param param_attr: The parameter attribute. See ParameterAttribute for details.\n    :type param_attr: ParameterAttribute\n    :param layer_attr: The extra layer attribute. See ExtraLayerAttribute for\n                       details.\n    :type layer_attr: ExtraLayerAttribute | None\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    '
    assert isinstance(input, LayerOutput), 'prelu_layer accepts only one input.'
    if (not param_attr):
        param_attr = ParamAttr(initial_mean=0.25, initial_std=0.0)
    else:
        assert isinstance(param_attr, ParameterAttribute)
    if (num_channels is None):
        assert (input.num_filters is not None), 'the input channel cannot be detected, please specify the num_channels parameter'
        num_channels = input.num_filters
    if (channel_shared is not None):
        assert isinstance(channel_shared, bool)
        assert ((input.height != 0) and (input.width != 0)), 'input height and widht must be setted'
        if channel_shared:
            partial_sum = ((input.height * input.width) * num_channels)
        else:
            partial_sum = (input.height * input.width)
    l = Layer(name=name, type=LayerType.PRELU, inputs=Input(input.name, **param_attr.attr), partial_sum=partial_sum, **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name=name, layer_type=LayerType.PRELU, parents=input, num_filters=num_channels, size=l.config.size)