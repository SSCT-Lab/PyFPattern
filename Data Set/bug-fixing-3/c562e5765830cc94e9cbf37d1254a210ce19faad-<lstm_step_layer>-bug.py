@wrap_bias_attr_default()
@wrap_act_default(param_names=['gate_act', 'state_act'], act=SigmoidActivation())
@wrap_act_default(act=TanhActivation())
@wrap_name_default('lstm_step')
@layer_support()
def lstm_step_layer(input, state, size, act=None, name=None, gate_act=None, state_act=None, bias_attr=None, layer_attr=None):
    "\n    LSTM Step Layer. It used in recurrent_group. The lstm equations are shown\n    as follow.\n\n    ..  math::\n\n        i_t & = \\sigma(W_{xi}x_{t} + W_{hi}h_{t-1} + W_{ci}c_{t-1} + b_i)\n\n        f_t & = \\sigma(W_{xf}x_{t} + W_{hf}h_{t-1} + W_{cf}c_{t-1} + b_f)\n\n        c_t & = f_tc_{t-1} + i_t tanh (W_{xc}x_t+W_{hc}h_{t-1} + b_c)\n\n        o_t & = \\sigma(W_{xo}x_{t} + W_{ho}h_{t-1} + W_{co}c_t + b_o)\n\n        h_t & = o_t tanh(c_t)\n\n\n    The input of lstm step is :math:`Wx_t + Wh_{t-1}`, and user should use\n    :code:`mixed_layer` and :code:`full_matrix_projection` to calculate these\n    input vector.\n\n    The state of lstm step is :math:`c_{t-1}`. And lstm step layer will do\n\n    ..  math::\n\n        i_t = \\sigma(input + W_{ci}c_{t-1} + b_i)\n\n        ...\n\n\n    This layer contains two outputs. Default output is :math:`h_t`. The other\n    output is :math:`o_t`, which name is 'state' and can use\n    :code:`get_output_layer` to extract this output.\n\n    :param name: Layer's name.\n    :type name: basestring\n    :param size: Layer's size. NOTE: lstm layer's size, should be equal as\n                 :code:`input.size/4`, and should be equal as\n                 :code:`state.size`.\n    :type size: int\n    :param input: input layer. :math:`Wx_t + Wh_{t-1}`\n    :type input: LayerOutput\n    :param state: State Layer. :math:`c_{t-1}`\n    :type state: LayerOutput\n    :param act: Activation type. Default is tanh\n    :type act: BaseActivation\n    :param gate_act: Gate Activation Type. Default is sigmoid, and should\n                          be sigmoid only.\n    :type gate_act: BaseActivation\n    :param state_act: State Activation Type. Default is sigmoid, and should\n                           be sigmoid only.\n    :type state_act: BaseActivation\n    :param bias_attr: Bias Attribute.\n    :type bias_attr: ParameterAttribute\n    :param layer_attr: layer's extra attribute.\n    :type layer_attr: ExtraLayerAttribute\n    :return: LayerOutput object.\n    :rtype: LayerOutput\n    "
    Layer(name=name, type=LayerType.LSTM_STEP_LAYER, active_type=act.name, active_gate_type=gate_act.name, active_state_type=state_act.name, bias=ParamAttr.to_bias(bias_attr), size=size, inputs=[input.name, state.name], **ExtraLayerAttribute.to_kwargs(layer_attr))
    return LayerOutput(name=name, layer_type=LayerType.LSTM_STEP_LAYER, parents=[input, state], activation=act, size=size, outputs=['default', 'state'])