def stack_bidirectional_rnn(cells_fw, cells_bw, inputs, initial_states_fw=None, initial_states_bw=None, dtype=None, sequence_length=None, scope=None):
    'Creates a bidirectional recurrent neural network.\n\n  Stacks several bidirectional rnn layers. The combined forward and backward\n  layer outputs are used as input of the next layer. tf.bidirectional_rnn\n  does not allow to share forward and backward information between layers.\n  The input_size of the first forward and backward cells must match.\n  The initial state for both directions is zero and no intermediate states\n  are returned.\n\n  As described in https://arxiv.org/abs/1303.5778\n\n  Args:\n    cells_fw: List of instances of RNNCell, one per layer,\n      to be used for forward direction.\n    cells_bw: List of instances of RNNCell, one per layer,\n      to be used for backward direction.\n    inputs: A length T list of inputs, each a tensor of shape\n      [batch_size, input_size], or a nested tuple of such elements.\n    initial_states_fw: (optional) A list of the initial states (one per layer)\n      for the forward RNN.\n      Each tensor must has an appropriate type and shape\n      `[batch_size, cell_fw.state_size]`.\n    initial_states_bw: (optional) Same as for `initial_states_fw`, but using\n      the corresponding properties of `cells_bw`.\n    dtype: (optional) The data type for the initial state.  Required if\n      either of the initial states are not provided.\n    sequence_length: (optional) An int32/int64 vector, size `[batch_size]`,\n      containing the actual lengths for each of the sequences.\n    scope: VariableScope for the created subgraph; defaults to None.\n\n  Returns:\n    A tuple (outputs, output_state_fw, output_state_bw) where:\n      outputs is a length `T` list of outputs (one for each input), which\n        are depth-concatenated forward and backward outputs.\n      output_states_fw is the final states, one tensor per layer,\n        of the forward rnn.\n      output_states_bw is the final states, one tensor per layer,\n        of the backward rnn.\n\n  Raises:\n    TypeError: If `cell_fw` or `cell_bw` is not an instance of `RNNCell`.\n    ValueError: If inputs is None, not a list or an empty list.\n  '
    if (not cells_fw):
        raise ValueError('Must specify at least one fw cell for BidirectionalRNN.')
    if (not cells_bw):
        raise ValueError('Must specify at least one bw cell for BidirectionalRNN.')
    if (not isinstance(cells_fw, list)):
        raise ValueError('cells_fw must be a list of RNNCells (one per layer).')
    if (not isinstance(cells_bw, list)):
        raise ValueError('cells_bw must be a list of RNNCells (one per layer).')
    if (len(cells_fw) != len(cells_bw)):
        raise ValueError('Forward and Backward cells must have the same depth.')
    if ((initial_states_fw is not None) and ((not isinstance(initial_states_fw, list)) or (len(initial_states_fw) != len(cells_fw)))):
        raise ValueError('initial_states_fw must be a list of state tensors (one per layer).')
    if ((initial_states_bw is not None) and ((not isinstance(initial_states_bw, list)) or (len(initial_states_bw) != len(cells_bw)))):
        raise ValueError('initial_states_bw must be a list of state tensors (one per layer).')
    states_fw = []
    states_bw = []
    prev_layer = inputs
    with vs.variable_scope((scope or 'stack_bidirectional_rnn')):
        for (i, (cell_fw, cell_bw)) in enumerate(zip(cells_fw, cells_bw)):
            initial_state_fw = None
            initial_state_bw = None
            if initial_states_fw:
                initial_state_fw = initial_states_fw[i]
            if initial_states_bw:
                initial_state_bw = initial_states_bw[i]
            with vs.variable_scope(('cell_%d' % i)) as cell_scope:
                (prev_layer, state_fw, state_bw) = rnn.static_bidirectional_rnn(cell_fw, cell_bw, prev_layer, initial_state_fw=initial_state_fw, initial_state_bw=initial_state_bw, sequence_length=sequence_length, dtype=dtype, scope=cell_scope)
            states_fw.append(state_fw)
            states_bw.append(state_bw)
    return (prev_layer, tuple(states_fw), tuple(states_bw))