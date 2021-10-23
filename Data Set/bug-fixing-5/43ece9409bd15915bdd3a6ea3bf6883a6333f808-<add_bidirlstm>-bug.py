def add_bidirlstm(self, name, W_h, W_x, b, W_h_back, W_x_back, b_back, hidden_size, input_size, input_names, output_names, inner_activation='SIGMOID', cell_state_update_activation='TANH', output_activation='TANH', peep=None, peep_back=None, output_all=False, forget_bias=False, coupled_input_forget_gate=False, cell_clip_threshold=50000.0):
    "\n        Add a Bi-directional LSTM layer to the model.\n\n        Parameters\n        ----------\n        name: str\n            The name of this layer.\n        W_h: [numpy.array]\n            List of recursion weight matrices for the forward layer. The ordering is [R_i, R_f, R_z, R_o],\n            where R_i, R_f, R_z, R_o are weight matrices at input gate, forget gate, cell gate and output gate.\n            The shapes of these matrices are (hidden_size, hidden_size).\n        W_x: [numpy.array]\n            List of input weight matrices for the forward layer. The ordering is [W_i, W_f, W_z, W_o],\n            where W_i, W_f, W_z, W_o are weight matrices at input gate, forget gate, cell gate and output gate.\n            The shapes of these matrices are (hidden_size, input_size).\n        b: [numpy.array]\n            List of biases for the forward layer. The ordering is [b_i, b_f, b_z, b_o],\n            where b_i, b_f, b_z, b_o are biases at input gate, forget gate, cell gate and output gate.\n            If None, biases are ignored. Otherwise the shapes of the biases are (hidden_size, ).\n        W_h_back: [numpy.array]\n            List of recursion weight matrices for the backward layer. The ordering is [R_i, R_f, R_z, R_o],\n            where R_i, R_f, R_z, R_o are weight matrices at input gate, forget gate, cell gate and output gate.\n            The shapes of these matrices are (hidden_size, hidden_size).\n        W_x_back: [numpy.array]\n            List of input weight matrices for the backward layer. The ordering is [W_i, W_f, W_z, W_o],\n            where W_i, W_f, W_z, W_o are weight matrices at input gate, forget gate, cell gate and output gate.\n            The shapes of these matrices are (hidden_size, input_size).\n        b_back: [numpy.array]\n            List of biases for the backward layer. The ordering is [b_i, b_f, b_z, b_o],\n            where b_i, b_f, b_z, b_o are biases at input gate, forget gate, cell gate and output gate.\n            The shapes of the biases (hidden_size).\n        hidden_size: int\n            Number of hidden units. This is equal to the number of channels of output shape.\n        input_size: int\n            Number of the number of channels of input shape.\n        input_names: [str]\n            The input blob name list of this layer, in the order of [x, h_input, c_input, h_reverse_input, c_reverse_input].\n        output_names: [str]\n            The output blob name list of this layer, in the order of [y, h_output, c_output, h_reverse_output, c_reverse_output].\n        inner_activation: str\n            Inner activation function used at input and forget gate. Can be one of the following option:\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n            Defaults to 'SIGMOID'. \n        cell_state_update_activation: str\n            Cell state update activation function used at the cell state update gate.\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n            Defaults to 'TANH'.\n        output_activation: str\n            Activation function used at the output gate. Can be one of the following option:\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n            Defaults to 'TANH'.\n        peep: [numpy.array] | None\n            List of peephole vectors for the forward layer. The ordering is [p_i, p_f, p_o],\n            where p_i, p_f, and p_o are peephole vectors at input gate, forget gate, output gate.\n            The shapes of the peephole vectors are (hidden_size,). Defaults to None.\n        peep_back: [numpy.array] | None\n            List of peephole vectors for the backward layer. The ordering is [p_i, p_f, p_o],\n            where p_i, p_f, and p_o are peephole vectors at input gate, forget gate, output gate.\n            The shapes of the peephole vectors are (hidden_size,). Defaults to None.\n        output_all: boolean\n            Whether the LSTM layer should output at every time step. Defaults to False.\n\n            - If False, the output is the result after the final state update.\n            - If True, the output is a sequence, containing outputs at all time steps.\n\n        forget_bias: boolean\n            If True, a vector of 1s is added to forget gate bias. Defaults to False.\n        coupled_input_forget_gate : boolean\n            If True, the inpute gate and forget gate is coupled. i.e. forget gate is not used.\n            Defaults to False.\n        cell_clip_threshold : float\n            The limit on the maximum and minimum values on the cell state.\n            Defaults to 50.0.\n\n        See Also\n        --------\n        add_activation, add_simple_rnn, add_unilstm, add_bidirlstm\n        "
    spec = self.spec
    nn_spec = self.nn_spec
    spec_layer = nn_spec.layers.add()
    spec_layer.name = name
    for name in input_names:
        spec_layer.input.append(name)
    for name in output_names:
        spec_layer.output.append(name)
    spec_layer_params = spec_layer.biDirectionalLSTM
    params = spec_layer_params.params
    weight_params = spec_layer_params.weightParams.add()
    weight_params_back = spec_layer_params.weightParams.add()
    spec_layer_params.inputVectorSize = input_size
    spec_layer_params.outputVectorSize = hidden_size
    if (b is not None):
        params.hasBiasVectors = True
    params.sequenceOutput = output_all
    params.forgetBias = forget_bias
    if (peep is not None):
        params.hasPeepholeVectors = True
    params.coupledInputAndForgetGate = coupled_input_forget_gate
    params.cellClipThreshold = cell_clip_threshold
    activation_f = spec_layer_params.activationsForwardLSTM.add()
    activation_g = spec_layer_params.activationsForwardLSTM.add()
    activation_h = spec_layer_params.activationsForwardLSTM.add()
    _set_recurrent_activation(activation_f, inner_activation)
    _set_recurrent_activation(activation_g, cell_state_update_activation)
    _set_recurrent_activation(activation_h, output_activation)
    activation_f_back = spec_layer_params.activationsBackwardLSTM.add()
    activation_g_back = spec_layer_params.activationsBackwardLSTM.add()
    activation_h_back = spec_layer_params.activationsBackwardLSTM.add()
    _set_recurrent_activation(activation_f_back, inner_activation)
    _set_recurrent_activation(activation_g_back, cell_state_update_activation)
    _set_recurrent_activation(activation_h_back, output_activation)
    (R_i, R_f, R_o, R_z) = W_h
    (W_i, W_f, W_o, W_z) = W_x
    weight_params.inputGateWeightMatrix.floatValue.extend(map(float, W_i.flatten()))
    weight_params.forgetGateWeightMatrix.floatValue.extend(map(float, W_f.flatten()))
    weight_params.outputGateWeightMatrix.floatValue.extend(map(float, W_o.flatten()))
    weight_params.blockInputWeightMatrix.floatValue.extend(map(float, W_z.flatten()))
    weight_params.inputGateRecursionMatrix.floatValue.extend(map(float, R_i.flatten()))
    weight_params.forgetGateRecursionMatrix.floatValue.extend(map(float, R_f.flatten()))
    weight_params.outputGateRecursionMatrix.floatValue.extend(map(float, R_o.flatten()))
    weight_params.blockInputRecursionMatrix.floatValue.extend(map(float, R_z.flatten()))
    if (b is not None):
        (b_i, b_f, b_o, b_z) = b
        weight_params.inputGateBiasVector.floatValue.extend(map(float, b_i.flatten()))
        weight_params.forgetGateBiasVector.floatValue.extend(map(float, b_f.flatten()))
        weight_params.outputGateBiasVector.floatValue.extend(map(float, b_o.flatten()))
        weight_params.blockInputBiasVector.floatValue.extend(map(float, b_z.flatten()))
    if (peep is not None):
        (p_i, p_f, p_o) = peep
        weight_params.inputGatePeepholeVector.floatValue.extend(map(float, p_i.flatten()))
        weight_params.forgetGatePeepholeVector.floatValue.extend(map(float, p_f.flatten()))
        weight_params.outputGatePeepholeVector.floatValue.extend(map(float, p_o.flatten()))
    (R_i, R_f, R_z, R_o) = W_h_back
    (W_i, W_f, W_z, W_o) = W_x_back
    weight_params_back.inputGateWeightMatrix.floatValue.extend(map(float, W_i.flatten()))
    weight_params_back.forgetGateWeightMatrix.floatValue.extend(map(float, W_f.flatten()))
    weight_params_back.outputGateWeightMatrix.floatValue.extend(map(float, W_z.flatten()))
    weight_params_back.blockInputWeightMatrix.floatValue.extend(map(float, W_o.flatten()))
    weight_params_back.inputGateRecursionMatrix.floatValue.extend(map(float, R_i.flatten()))
    weight_params_back.forgetGateRecursionMatrix.floatValue.extend(map(float, R_f.flatten()))
    weight_params_back.outputGateRecursionMatrix.floatValue.extend(map(float, R_z.flatten()))
    weight_params_back.blockInputRecursionMatrix.floatValue.extend(map(float, R_o.flatten()))
    if (b_back is not None):
        (b_i, b_f, b_z, b_o) = b_back
        weight_params_back.inputGateBiasVector.floatValue.extend(map(float, b_i.flatten()))
        weight_params_back.forgetGateBiasVector.floatValue.extend(map(float, b_f.flatten()))
        weight_params_back.outputGateBiasVector.floatValue.extend(map(float, b_z.flatten()))
        weight_params_back.blockInputBiasVector.floatValue.extend(map(float, b_o.flatten()))
    if (peep_back is not None):
        (p_i, p_f, p_o) = peep_back
        weight_params_back.inputGatePeepholeVector.floatValue.extend(map(float, p_i.flatten()))
        weight_params_back.forgetGatePeepholeVector.floatValue.extend(map(float, p_f.flatten()))
        weight_params_back.outputGatePeepholeVector.floatValue.extend(map(float, p_o.flatten()))