def rnn(step_function, inputs, initial_states, go_backwards=False, mask=None, constants=None, unroll=False, input_length=None):
    "Iterates over the time dimension of a tensor.\n\n    # Arguments\n        inputs: tensor of temporal data of shape (samples, time, ...)\n            (at least 3D).\n        step_function:\n            Parameters:\n                input: tensor with shape (samples, ...) (no time dimension),\n                    representing input for the batch of samples at a certain\n                    time step.\n                states: list of tensors.\n            Returns:\n                output: tensor with shape (samples, output_dim) (no time dimension),\n                new_states: list of tensors, same length and shapes\n                    as 'states'. The first state in the list must be the\n                    output tensor at the previous timestep.\n        initial_states: tensor with shape (samples, output_dim) (no time dimension),\n            containing the initial values for the states used in\n            the step function.\n        go_backwards: boolean. If True, do the iteration over\n            the time dimension in reverse order.\n        mask: binary tensor with shape (samples, time, 1),\n            with a zero for every element that is masked.\n        constants: a list of constant values passed at each step.\n        unroll: with TensorFlow the RNN is always unrolled, but with Theano you\n            can use this boolean flag to unroll the RNN.\n        input_length: not relevant in the TensorFlow implementation.\n            Must be specified if using unrolling with Theano.\n\n    # Returns\n        A tuple (last_output, outputs, new_states).\n\n        last_output: the latest output of the rnn, of shape (samples, ...)\n        outputs: tensor with shape (samples, time, ...) where each\n            entry outputs[s, t] is the output of the step function\n            at time t for sample s.\n        new_states: list of tensors, latest states returned by\n            the step function, of shape (samples, ...).\n    "
    ndim = len(inputs.get_shape())
    assert (ndim >= 3), 'Input should be at least 3D.'
    axes = ([1, 0] + list(range(2, ndim)))
    inputs = tf.transpose(inputs, axes)
    if (constants is None):
        constants = []
    if unroll:
        if (not inputs.get_shape()[0]):
            raise Exception('Unrolling requires a fixed number of timesteps.')
        states = initial_states
        successive_states = []
        successive_outputs = []
        input_list = tf.unpack(inputs)
        if go_backwards:
            input_list.reverse()
        if (mask is not None):
            mask = tf.cast(mask, tf.uint8)
            if (len(mask.get_shape()) == (ndim - 1)):
                mask = expand_dims(mask)
            mask = tf.cast(tf.transpose(mask, axes), tf.bool)
            mask_list = tf.unpack(mask)
            if go_backwards:
                mask_list.reverse()
            for (input, mask_t) in zip(input_list, mask_list):
                (output, new_states) = step_function(input, (states + constants))
                tiled_mask_t = tf.tile(mask_t, tf.pack([1, tf.shape(output)[1]]))
                if (len(successive_outputs) == 0):
                    prev_output = zeros_like(output)
                else:
                    prev_output = successive_outputs[(- 1)]
                output = tf.select(tiled_mask_t, output, prev_output)
                return_states = []
                for (state, new_state) in zip(states, new_states):
                    tiled_mask_t = tf.tile(mask_t, tf.pack([1, tf.shape(new_state)[1]]))
                    return_states.append(tf.select(tiled_mask_t, new_state, state))
                states = return_states
                successive_outputs.append(output)
                successive_states.append(states)
                last_output = successive_outputs[(- 1)]
                new_states = successive_states[(- 1)]
                outputs = tf.pack(successive_outputs)
        else:
            for input in input_list:
                (output, states) = step_function(input, (states + constants))
                successive_outputs.append(output)
                successive_states.append(states)
            last_output = successive_outputs[(- 1)]
            new_states = successive_states[(- 1)]
            outputs = tf.pack(successive_outputs)
    else:
        from tensorflow.python.ops.rnn import _dynamic_rnn_loop
        if go_backwards:
            inputs = tf.reverse(inputs, ([True] + ([False] * (ndim - 1))))
        states = initial_states
        nb_states = len(states)
        if (nb_states == 0):
            raise Exception('No initial states provided.')
        elif (nb_states == 1):
            state = states[0]
        else:
            state = tf.concat(1, states)
        state_size = int(states[0].get_shape()[(- 1)])
        if (mask is not None):
            if go_backwards:
                mask = tf.reverse(mask, ([True] + ([False] * (ndim - 2))))
            mask = tf.cast(mask, tf.uint8)
            if (len(mask.get_shape()) == (ndim - 1)):
                mask = expand_dims(mask)
            mask = tf.transpose(mask, axes)
            inputs = tf.concat(2, [tf.cast(mask, inputs.dtype), inputs])

            def _step(input, state):
                if (nb_states > 1):
                    states = []
                    for i in range(nb_states):
                        states.append(state[:, (i * state_size):((i + 1) * state_size)])
                else:
                    states = [state]
                mask_t = tf.cast(input[:, 0], tf.bool)
                input = input[:, 1:]
                (output, new_states) = step_function(input, (states + constants))
                output = tf.select(mask_t, output, states[0])
                new_states = [tf.select(mask_t, new_states[i], states[i]) for i in range(len(states))]
                if (len(new_states) == 1):
                    new_state = new_states[0]
                else:
                    new_state = tf.concat(1, new_states)
                return (output, new_state)
        else:

            def _step(input, state):
                if (nb_states > 1):
                    states = []
                    for i in range(nb_states):
                        states.append(state[:, (i * state_size):((i + 1) * state_size)])
                else:
                    states = [state]
                (output, new_states) = step_function(input, (states + constants))
                if (len(new_states) == 1):
                    new_state = new_states[0]
                else:
                    new_state = tf.concat(1, new_states)
                return (output, new_state)
        _step.state_size = (state_size * nb_states)
        _step.output_size = state_size
        (outputs, final_state) = _dynamic_rnn_loop(_step, inputs, state, parallel_iterations=32, swap_memory=True, sequence_length=None)
        if (nb_states > 1):
            new_states = []
            for i in range(nb_states):
                new_states.append(final_state[:, (i * state_size):((i + 1) * state_size)])
        else:
            new_states = [final_state]
        begin = tf.pack(([(tf.shape(outputs)[0] - 1)] + ([0] * (ndim - 1))))
        size = tf.pack(([1] + ([(- 1)] * (ndim - 1))))
        last_output = tf.slice(outputs, begin, size)
        last_output = tf.squeeze(last_output, [0])
    axes = ([1, 0] + list(range(2, len(outputs.get_shape()))))
    outputs = tf.transpose(outputs, axes)
    return (last_output, outputs, new_states)