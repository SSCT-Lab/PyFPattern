

def gru_unit(input, hidden, size, weight=None, bias=None, activation='tanh', gate_activation='sigmoid'):
    "\n    GRU unit layer. The equation of a gru step is:\n\n        .. math::\n            u_t & = actGate(xu_{t} + W_u h_{t-1} + b_u)\n\n            r_t & = actGate(xr_{t} + W_r h_{t-1} + b_r)\n\n            m_t & = actNode(xm_t + W_c dot(r_t, h_{t-1}) + b_m)\n\n            h_t & = dot((1-u_t), m_t) + dot(u_t, h_{t-1})\n\n    The inputs of gru unit includes :math:`z_t`, :math:`h_{t-1}`. In terms\n    of the equation above, the :math:`z_t` is split into 3 parts - \n    :math:`xu_t`, :math:`xr_t` and :math:`xm_t`. This means that in order to \n    implement a full GRU unit operator for an input, a fully \n    connected layer has to be applied, such that :math:`z_t = W_{fc}x_t`.\n\n    The terms :math:`u_t` and :math:`r_t` represent the update and reset gates \n    of the GRU cell. Unlike LSTM, GRU has one lesser gate. However, there is \n    an intermediate candidate hidden output, which is denoted by :math:`m_t`.\n    This layer has three outputs :math:`h_t`, :math:`dot(r_t, h_{t-1})`\n    and concatenation of :math:`u_t`, :math:`r_t` and :math:`m_t`.\n\n    Args:\n        input (Variable): The fc transformed input value of current step.\n        hidden (Variable): The hidden value of lstm unit from previous step.\n        size (integer): The input dimension value.\n        weight (ParamAttr): The weight parameters for gru unit. Default: None\n        bias (ParamAttr): The bias parameters for gru unit. Default: None\n        activation (string): The activation type for cell (actNode). Default: 'tanh'\n        gate_activation (string): The activation type for gates (actGate). Default: 'sigmoid'\n\n    Returns:\n        tuple: The hidden value, reset-hidden value and gate values.\n\n    Examples:\n\n        .. code-block:: python\n\n             # assuming we have x_t_data and prev_hidden of size=10\n             x_t = fluid.layers.fc(input=x_t_data, size=30) \n             hidden_val, r_h_val, gate_val = fluid.layers.gru_unit(input=x_t,\n                                                    hidden = prev_hidden)\n\n    "
    activation_dict = dict(identity=0, sigmoid=1, tanh=2, relu=3)
    activation = activation_dict[activation]
    gate_activation = activation_dict[gate_activation]
    helper = LayerHelper('gru_unit', **locals())
    dtype = helper.input_dtype()
    size = (size / 3)
    if (weight is None):
        weight = helper.create_parameter(attr=helper.param_attr, shape=[size, (3 * size)], dtype=dtype)
    if (bias is None):
        bias_size = [1, (3 * size)]
        bias = helper.create_parameter(attr=helper.bias_attr, shape=bias_size, dtype=dtype, is_bias=True)
    gate = helper.create_tmp_variable(dtype)
    reset_hidden_pre = helper.create_tmp_variable(dtype)
    updated_hidden = helper.create_tmp_variable(dtype)
    helper.append_op(type='gru_unit', inputs={
        'Input': input,
        'HiddenPrev': hidden,
        'Weight': weight,
    }, outputs={
        'Gate': gate,
        'ResetHiddenPrev': reset_hidden_pre,
        'Hidden': updated_hidden,
    }, attrs={
        'activation': 0,
        'gate_activation': 1,
    })
    return (updated_hidden, reset_hidden_pre, gate)
