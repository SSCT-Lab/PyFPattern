def add_unilstm(self, name, W_h, W_x, b, hidden_size, input_size, input_names, output_names, inner_activation='SIGMOID', cell_state_update_activation='TANH', output_activation='TANH', peep=None, output_all=False, forget_bias=False, coupled_input_forget_gate=False, cell_clip_threshold=50000.0, reverse_input=False):
    "\n        Add a Uni-directional LSTM layer to the model.\n\n        Parameters\n        ----------\n        name: str\n            The name of this layer.\n        W_h: [numpy.array]\n            List of recursion weight matrices. The ordering is [R_i, R_f, R_o, R_z],\n            where R_i, R_f, R_o, R_z are weight matrices at input gate, forget gate, output gate and cell gate.\n            The shapes of these matrices are (hidden_size, hidden_size).\n        W_x: [numpy.array]\n            List of input weight matrices. The ordering is [W_i, W_f, W_o, W_z],\n            where W_i, W_f, W_o, W_z are weight matrices at input gate, forget gate, output gate and cell gate.\n            The shapes of these matrices are (hidden_size, input_size).\n        b: [numpy.array] | None\n            List of biases. The ordering is [b_i, b_f, b_o, b_z],\n            where b_i, b_f, b_o, b_z are biases at input gate, forget gate, output gate and cell gate.\n            If None, biases are ignored. Otherwise the shapes of the biases are (hidden_size, ).\n        hidden_size: int\n            Number of hidden units. This is equal to the number of channels of output shape.\n        input_size: int\n            Number of the number of channels of input shape.\n        input_names: [str]\n            The input blob name list of this layer, in the order of [x, h_input, c_input].\n        output_names: [str]\n            The output blob name list of this layer, in the order of [y, h_output, c_output].\n        inner_activation: str\n            Inner activation function used at input and forget gate. Can be one of the following option:\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n        cell_state_update_activation: str\n            Cell state update activation function used at the cell state update gate.\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n        output_activation: str\n            Activation function used at the output gate. Can be one of the following option:\n            ['RELU', 'TANH', 'SIGMOID', 'SCALED_TANH', 'SIGMOID_HARD', 'LINEAR'].\n        peep: [numpy.array] | None\n            List of peephole vectors. The ordering is [p_i, p_f, p_o],\n            where p_i, p_f, and p_o are peephole vectors at input gate, forget gate, output gate.\n            The shapes of the peephole vectors are (hidden_size,).\n        output_all: boolean\n            Whether the LSTM layer should output at every time step.\n\n            - If False, the output is the result after the final state update.\n            - If True, the output is a sequence, containing outputs at all time steps.\n\n        forget_bias: boolean\n            If True, a vector of 1s is added to forget gate bias.\n        coupled_input_forget_gate: boolean\n            If True, the inpute gate and forget gate is coupled. i.e. forget gate is not used.\n        cell_clip_threshold: float\n            The limit on the maximum and minimum values on the cell state.\n            If not provided, it is defaulted to 50.0.\n        reverse_input: boolean\n            Whether the LSTM layer should process the input sequence in the reverse order.\n\n            - If False, the input sequence order is not reversed.\n            - If True, the input sequence order is reversed.\n\n        See Also\n        --------\n        add_activation, add_simple_rnn, add_gru, add_bidirlstm\n        "
    spec = self.spec
    nn_spec = self.nn_spec
    spec_layer = nn_spec.layers.add()
    spec_layer.name = name
    for name in input_names:
        spec_layer.input.append(name)
    for name in output_names:
        spec_layer.output.append(name)
    spec_layer_params = spec_layer.uniDirectionalLSTM
    params = spec_layer_params.params
    weight_params = spec_layer_params.weightParams
    spec_layer_params.inputVectorSize = input_size
    spec_layer_params.outputVectorSize = hidden_size
    params.sequenceOutput = output_all
    params.forgetBias = False
    if (b is not None):
        params.hasBiasVectors = True
    if (peep is not None):
        params.hasPeepholeVectors = True
    params.coupledInputAndForgetGate = coupled_input_forget_gate
    params.cellClipThreshold = cell_clip_threshold
    params.forgetBias = forget_bias
    spec_layer_params.reverseInput = reverse_input
    activation_f = spec_layer_params.activations.add()
    activation_g = spec_layer_params.activations.add()
    activation_h = spec_layer_params.activations.add()
    _set_recurrent_activation(activation_f, inner_activation)
    _set_recurrent_activation(activation_g, cell_state_update_activation)
    _set_recurrent_activation(activation_h, output_activation)
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