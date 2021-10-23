@wrap_name_default('simple_gru2')
def simple_gru2(input, size, name=None, reverse=False, mixed_param_attr=None, mixed_bias_attr=None, gru_param_attr=None, gru_bias_attr=None, act=None, gate_act=None, mixed_layer_attr=None, gru_cell_attr=None):
    '\n    simple_gru2 is the same with simple_gru, but using grumemory instead\n    Please see grumemory in layers.py for more detail about the maths.\n    simple_gru2 is faster than simple_gru.\n\n    The example usage is:\n\n    ..  code-block:: python\n\n        gru = simple_gru2(input=[layer1], size=256)\n\n    :param input: input layer name.\n    :type input: LayerOutput\n    :param name: name of the gru group.\n    :type name: basestring\n    :param size: hidden size of the gru.\n    :type size: int\n    :param reverse: whether to process the input data in a reverse order\n    :type reverse: bool\n    :param act: type of the activiation\n    :type act: BaseActivation\n    :param gate_act: type of the gate activiation\n    :type gate_act: BaseActivation\n    :param gru_bias_attr: bias. False means no bias, None means default bias.\n    :type gru_bias_attr: ParameterAttribute|False\n    :param gru_layer_attr: Extra parameter attribute of the gru layer.\n    :type gru_layer_attr: ParameterAttribute|False\n    :return: the gru group.\n    :rtype: LayerOutput\n    '
    with mixed_layer(name=('%s_transform' % name), size=(size * 3), bias_attr=mixed_bias_attr, layer_attr=mixed_layer_attr) as m:
        m += full_matrix_projection(input=input, param_attr=mixed_param_attr)
    return grumemory(name=name, input=m, reverse=reverse, bias_attr=gru_bias_attr, param_attr=gru_param_attr, act=act, gate_act=gate_act, layer_attr=gru_cell_attr)