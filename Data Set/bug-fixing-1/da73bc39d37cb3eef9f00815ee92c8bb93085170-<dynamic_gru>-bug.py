

def dynamic_gru(input, size, param_attr=None, bias_attr=None, is_reverse=False, gate_activation='sigmoid', candidate_activation='tanh', h_0=None):
    '\n    **Gated Recurrent Unit (GRU) Layer**\n\n    Refer to `Empirical Evaluation of Gated Recurrent Neural Networks on\n    Sequence Modeling <https://arxiv.org/abs/1412.3555>`_ .\n\n    The formula is as follows:\n\n    .. math::\n\n        u_t & = act_g(W_{ux}x_{t} + W_{uh}h_{t-1} + b_u)\n\n        r_t & = act_g(W_{rx}x_{t} + W_{rh}h_{t-1} + b_r)\n\n        \\tilde{h_t} & = act_c(W_{cx}x_{t} + W_{ch}(r_t \\odot h_{t-1}) + b_c)\n\n        h_t & = (1-u_t) \\odot h_{t-1} + u_t \\odot \\tilde{h_t}\n\n    The :math:`\\odot` is the element-wise product of the vectors. :math:`act_g`\n    is the update gate and reset gate activation function and :math:`sigmoid`\n    is usually used for it. :math:`act_c` is the activation function for\n    candidate hidden state and :math:`tanh` is usually used for it.\n\n    Note that these :math:`W_{ux}x_{t}, W_{rx}x_{t}, W_{cx}x_{t}` operations on\n    the input :math:`x_{t}` are NOT included in this operator. Users can choose\n    to use fully-connect layer before GRU layer.\n\n    Args:\n        input(Variable): The input of dynamic_gru layer, which supports\n            variable-time length input sequence. The underlying tensor in this\n            Variable is a matrix with shape :math:`(T \\times 3D)`, where\n            :math:`T` is the total time steps in this mini-batch, :math:`D`\n            is the hidden size.\n        size(int): The dimension of the gru cell.\n        param_attr(ParamAttr|None): The parameter attribute for the learnable\n            hidden-hidden weight matrix. Note:\n\n            - The shape of the weight matrix is :math:`(T \\times 3D)`, where\n              :math:`D` is the hidden size.\n            - All elements in the weight matrix can be divided into two parts.\n              The first part are weights of the update gate and reset gate with\n              shape :math:`(D \\times 2D)`, and the second part are weights for\n              candidate hidden state with shape :math:`(D \\times D)`.\n        bias_attr(ParamAttr): The parameter attribute for learnable the\n            hidden-hidden bias.\n        is_reverse(bool): Whether to compute reversed GRU, default\n            :attr:`False`.\n        gate_activation(str): The activation for update gate and reset gate.\n            Choices = ["sigmoid", "tanh", "relu", "identity"], default "sigmoid".\n        candidate_activation(str): The activation for candidate hidden state.\n            Choices = ["sigmoid", "tanh", "relu", "identity"], default "tanh".\n        h_0 (Variable): This is initial hidden state. If not set, default is\n            zero. This is a tensor with shape (N x D), where N is the number of\n            total time steps of input mini-batch feature and D is the hidden\n            size.\n\n    Returns:\n        Variable: The hidden state of GRU. The shape is :math:`(T \\times D)`,             and sequence length is the same with the input.\n\n    Examples:\n\n        .. code-block:: python\n\n            dict_dim, emb_dim = 128, 64\n            data = fluid.layers.data(name=\'sequence\', shape=[1],\n                                     dtype=\'int32\', lod_level=1)\n            emb = fluid.layers.embedding(input=data, size=[dict_dim, emb_dim])\n            hidden_dim = 512\n            x = fluid.layers.fc(input=emb, size=hidden_dim * 3)\n            hidden = fluid.layers.dynamic_gru(input=x, dim=hidden_dim)\n    '
    helper = LayerHelper('gru', **locals())
    dtype = helper.input_dtype()
    weight = helper.create_parameter(attr=helper.param_attr, shape=[size, (3 * size)], dtype=dtype)
    bias = helper.create_parameter(attr=helper.bias_attr, shape=[1, (3 * size)], dtype=dtype, is_bias=True)
    batch_size = input.shape[0]
    inputs = {
        'Input': input,
        'Weight': weight,
        'Bias': bias,
    }
    if (h_0 != None):
        assert (h_0.shape == (batch_size, size)), ('The shape of h0 should be(batch_size, %d)' % size)
        inputs['H0'] = h_0
    hidden = helper.create_variable_for_type_inference(dtype)
    batch_gate = helper.create_variable_for_type_inference(dtype)
    batch_reset_hidden_prev = helper.create_variable_for_type_inference(dtype)
    batch_hidden = helper.create_variable_for_type_inference(dtype)
    helper.append_op(type='gru', inputs=inputs, outputs={
        'Hidden': hidden,
        'BatchGate': batch_gate,
        'BatchResetHiddenPrev': batch_reset_hidden_prev,
        'BatchHidden': batch_hidden,
    }, attrs={
        'is_reverse': is_reverse,
        'gate_activation': gate_activation,
        'activation': candidate_activation,
    })
    return hidden
