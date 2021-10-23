def embedding_rnn_seq2seq(encoder_inputs, decoder_inputs, cell, num_encoder_symbols, num_decoder_symbols, embedding_size, output_projection=None, feed_previous=False, dtype=None, scope=None):
    'Embedding RNN sequence-to-sequence model.\n\n  This model first embeds encoder_inputs by a newly created embedding (of shape\n  [num_encoder_symbols x input_size]). Then it runs an RNN to encode\n  embedded encoder_inputs into a state vector. Next, it embeds decoder_inputs\n  by another newly created embedding (of shape [num_decoder_symbols x\n  input_size]). Then it runs RNN decoder, initialized with the last\n  encoder state, on embedded decoder_inputs.\n\n  Args:\n    encoder_inputs: A list of 1D int32 Tensors of shape [batch_size].\n    decoder_inputs: A list of 1D int32 Tensors of shape [batch_size].\n    cell: rnn_cell.RNNCell defining the cell function and size.\n    num_encoder_symbols: Integer; number of symbols on the encoder side.\n    num_decoder_symbols: Integer; number of symbols on the decoder side.\n    embedding_size: Integer, the length of the embedding vector for each symbol.\n    output_projection: None or a pair (W, B) of output projection weights and\n      biases; W has shape [output_size x num_decoder_symbols] and B has\n      shape [num_decoder_symbols]; if provided and feed_previous=True, each\n      fed previous output will first be multiplied by W and added B.\n    feed_previous: Boolean or scalar Boolean Tensor; if True, only the first\n      of decoder_inputs will be used (the "GO" symbol), and all other decoder\n      inputs will be taken from previous outputs (as in embedding_rnn_decoder).\n      If False, decoder_inputs are used as given (the standard decoder case).\n    dtype: The dtype of the initial state for both the encoder and encoder\n      rnn cells (default: tf.float32).\n    scope: VariableScope for the created subgraph; defaults to\n      "embedding_rnn_seq2seq"\n\n  Returns:\n    A tuple of the form (outputs, state), where:\n      outputs: A list of the same length as decoder_inputs of 2D Tensors. The\n        output is of shape [batch_size x cell.output_size] when\n        output_projection is not None (and represents the dense representation\n        of predicted tokens). It is of shape [batch_size x num_decoder_symbols]\n        when output_projection is None.\n      state: The state of each decoder cell in each time-step. This is a list\n        with length len(decoder_inputs) -- one item for each time-step.\n        It is a 2D Tensor of shape [batch_size x cell.state_size].\n  '
    with variable_scope.variable_scope((scope or 'embedding_rnn_seq2seq')) as scope:
        if (dtype is not None):
            scope.set_dtype(dtype)
        else:
            dtype = scope.dtype
        encoder_cell = rnn_cell.EmbeddingWrapper(cell, embedding_classes=num_encoder_symbols, embedding_size=embedding_size)
        (_, encoder_state) = rnn.rnn(encoder_cell, encoder_inputs, dtype=dtype)
        if (output_projection is None):
            cell = rnn_cell.OutputProjectionWrapper(cell, num_decoder_symbols)
        if isinstance(feed_previous, bool):
            return embedding_rnn_decoder(decoder_inputs, encoder_state, cell, num_decoder_symbols, embedding_size, output_projection=output_projection, feed_previous=feed_previous)

        def decoder(feed_previous_bool):
            reuse = (None if feed_previous_bool else True)
            with variable_scope.variable_scope(variable_scope.get_variable_scope(), reuse=reuse) as scope:
                (outputs, state) = embedding_rnn_decoder(decoder_inputs, encoder_state, cell, num_decoder_symbols, embedding_size, output_projection=output_projection, feed_previous=feed_previous_bool, update_embedding_for_previous=False)
                state_list = [state]
                if nest.is_sequence(state):
                    state_list = nest.flatten(state)
                return (outputs + state_list)
        outputs_and_state = control_flow_ops.cond(feed_previous, (lambda : decoder(True)), (lambda : decoder(False)))
        outputs_len = len(decoder_inputs)
        state_list = outputs_and_state[outputs_len:]
        state = state_list[0]
        if nest.is_sequence(encoder_state):
            state = nest.pack_sequence_as(structure=encoder_state, flat_sequence=state_list)
        return (outputs_and_state[:outputs_len], state)