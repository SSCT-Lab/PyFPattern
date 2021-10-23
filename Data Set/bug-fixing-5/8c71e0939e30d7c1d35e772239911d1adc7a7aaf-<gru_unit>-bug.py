@wrap_name_default('gru_unit')
def gru_unit(input, memory_boot=None, size=None, name=None, gru_bias_attr=None, gru_param_attr=None, act=None, gate_act=None, gru_layer_attr=None, naive=False):
    '\n    Define calculations that a gated recurrent unit performs in a single time\n    step. This function itself is not a recurrent layer, so it can not be\n    directly used to process sequence inputs. This function is always used in\n    the recurrent_group (see layers.py for more details) to implement attention\n    mechanism.\n\n    Please see grumemory in layers.py for the details about the maths.\n\n    :param input: input layer name.\n    :type input: LayerOutput\n    :param memory_boot: the initialization state of the LSTM cell.\n    :type memory_boot: LayerOutput | None\n    :param name: name of the gru group.\n    :type name: basestring\n    :param size: hidden size of the gru.\n    :type size: int\n    :param act: type of the activation\n    :type act: BaseActivation\n    :param gate_act: type of the gate activation\n    :type gate_act: BaseActivation\n    :param gru_layer_attr: Extra parameter attribute of the gru layer.\n    :type gru_layer_attr: ParameterAttribute|False\n    :return: the gru output layer.\n    :rtype: LayerOutput\n    '
    assert ((input.size % 3) == 0)
    if (size is None):
        size = (input.size / 3)
    out_mem = memory(name=name, size=size, boot_layer=memory_boot)
    if naive:
        __step__ = gru_step_naive_layer
    else:
        __step__ = gru_step_layer
    gru_out = __step__(name=name, input=input, output_mem=out_mem, size=size, bias_attr=gru_bias_attr, param_attr=gru_param_attr, act=act, gate_act=gate_act, layer_attr=gru_layer_attr)
    return gru_out