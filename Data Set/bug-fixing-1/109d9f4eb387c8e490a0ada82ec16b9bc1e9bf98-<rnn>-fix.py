

def rnn(step_function, inputs, initial_states, go_backwards=False, mask=None, constants=None, unroll=False, input_length=None):
    "Iterates over the time dimension of a tensor.\n\n    # Arguments\n        step_function: RNN step function.\n            Parameters:\n                input: tensor with shape `(samples, ...)` (no time dimension),\n                    representing input for the batch of samples at a certain\n                    time step.\n                states: list of tensors.\n            Returns:\n                output: tensor with shape `(samples, output_dim)`\n                    (no time dimension).\n                new_states: list of tensors, same length and shapes\n                    as 'states'. The first state in the list must be the\n                    output tensor at the previous timestep.\n        inputs: tensor of temporal data of shape `(samples, time, ...)`\n            (at least 3D).\n        initial_states: tensor with shape (samples, output_dim)\n            (no time dimension),\n            containing the initial values for the states used in\n            the step function.\n        go_backwards: boolean. If True, do the iteration over\n            the time dimension in reverse order.\n        mask: binary tensor with shape `(samples, time, 1)`,\n            with a zero for every element that is masked.\n        constants: a list of constant values passed at each step.\n        unroll: whether to unroll the RNN or to use a symbolic loop (`while_loop` or `scan` depending on backend).\n        input_length: not relevant in the TensorFlow implementation.\n            Must be specified if using unrolling with Theano.\n\n    # Returns\n        A tuple, `(last_output, outputs, new_states)`.\n\n            last_output: the latest output of the rnn, of shape `(samples, ...)`\n            outputs: tensor with shape `(samples, time, ...)` where each\n                entry `outputs[s, t]` is the output of the step function\n                at time `t` for sample `s`.\n            new_states: list of tensors, latest states returned by\n                the step function, of shape `(samples, ...)`.\n\n    # Raises\n        ValueError: if input dimension is less than 3.\n        ValueError: if `unroll` is `True` but input timestep is not a fixed number.\n        ValueError: if `mask` is provided (not `None`) but states is not provided\n            (`len(states)` == 0).\n    "
    ndim = len(inputs.get_shape())
    if (ndim < 3):
        raise ValueError('Input should be at least 3D.')
    axes = ([1, 0] + list(range(2, ndim)))
    inputs = tf.transpose(inputs, axes)
    if (mask is not None):
        if (mask.dtype != tf.bool):
            mask = tf.cast(mask, tf.bool)
        if (len(mask.get_shape()) == (ndim - 1)):
            mask = expand_dims(mask)
        mask = tf.transpose(mask, axes)
    if (constants is None):
        constants = []
    if unroll:
        if (not inputs.get_shape()[0]):
            raise ValueError('Unrolling requires a fixed number of timesteps.')
        states = initial_states
        successive_states = []
        successive_outputs = []
        input_list = tf.unstack(inputs)
        if go_backwards:
            input_list.reverse()
        if (mask is not None):
            mask_list = tf.unstack(mask)
            if go_backwards:
                mask_list.reverse()
            for (inp, mask_t) in zip(input_list, mask_list):
                (output, new_states) = step_function(inp, (states + constants))
                tiled_mask_t = tf.tile(mask_t, tf.stack([1, tf.shape(output)[1]]))
                if (not successive_outputs):
                    prev_output = zeros_like(output)
                else:
                    prev_output = successive_outputs[(- 1)]
                output = tf.where(tiled_mask_t, output, prev_output)
                return_states = []
                for (state, new_state) in zip(states, new_states):
                    tiled_mask_t = tf.tile(mask_t, tf.stack([1, tf.shape(new_state)[1]]))
                    return_states.append(tf.where(tiled_mask_t, new_state, state))
                states = return_states
                successive_outputs.append(output)
                successive_states.append(states)
            last_output = successive_outputs[(- 1)]
            new_states = successive_states[(- 1)]
            outputs = tf.stack(successive_outputs)
        else:
            for inp in input_list:
                (output, states) = step_function(inp, (states + constants))
                successive_outputs.append(output)
                successive_states.append(states)
            last_output = successive_outputs[(- 1)]
            new_states = successive_states[(- 1)]
            outputs = tf.stack(successive_outputs)
    else:
        if go_backwards:
            inputs = reverse(inputs, 0)
        states = tuple(initial_states)
        time_steps = tf.shape(inputs)[0]
        (outputs, _) = step_function(inputs[0], (initial_states + constants))
        output_ta = tensor_array_ops.TensorArray(dtype=outputs.dtype, size=time_steps, tensor_array_name='output_ta')
        input_ta = tensor_array_ops.TensorArray(dtype=inputs.dtype, size=time_steps, tensor_array_name='input_ta')
        input_ta = input_ta.unstack(inputs)
        time = tf.constant(0, dtype='int32', name='time')
        if (mask is not None):
            if (not states):
                raise ValueError('No initial states provided! When using masking in an RNN, you should provide initial states (and your step function should return as its first state at time `t` the output at time `t-1`).')
            if go_backwards:
                mask = reverse(mask, 0)
            mask_ta = tensor_array_ops.TensorArray(dtype=tf.bool, size=time_steps, tensor_array_name='mask_ta')
            mask_ta = mask_ta.unstack(mask)

            def _step(time, output_ta_t, *states):
                'RNN step function.\n\n                # Arguments\n                    time: Current timestep value.\n                    output_ta_t: TensorArray.\n                    *states: List of states.\n\n                # Returns\n                    Tuple: `(time + 1,output_ta_t) + tuple(new_states)`\n                '
                current_input = input_ta.read(time)
                mask_t = mask_ta.read(time)
                (output, new_states) = step_function(current_input, (tuple(states) + tuple(constants)))
                for (state, new_state) in zip(states, new_states):
                    new_state.set_shape(state.get_shape())
                tiled_mask_t = tf.tile(mask_t, tf.stack([1, tf.shape(output)[1]]))
                output = tf.where(tiled_mask_t, output, states[0])
                new_states = [tf.where(tiled_mask_t, new_states[i], states[i]) for i in range(len(states))]
                output_ta_t = output_ta_t.write(time, output)
                return (((time + 1), output_ta_t) + tuple(new_states))
        else:

            def _step(time, output_ta_t, *states):
                'RNN step function.\n\n                # Arguments\n                    time: Current timestep value.\n                    output_ta_t: TensorArray.\n                    *states: List of states.\n\n                # Returns\n                    Tuple: `(time + 1,output_ta_t) + tuple(new_states)`\n                '
                current_input = input_ta.read(time)
                (output, new_states) = step_function(current_input, (tuple(states) + tuple(constants)))
                for (state, new_state) in zip(states, new_states):
                    new_state.set_shape(state.get_shape())
                output_ta_t = output_ta_t.write(time, output)
                return (((time + 1), output_ta_t) + tuple(new_states))
        final_outputs = control_flow_ops.while_loop(cond=(lambda time, *_: (time < time_steps)), body=_step, loop_vars=((time, output_ta) + states), parallel_iterations=32, swap_memory=True)
        last_time = final_outputs[0]
        output_ta = final_outputs[1]
        new_states = final_outputs[2:]
        outputs = output_ta.stack()
        last_output = output_ta.read((last_time - 1))
    axes = ([1, 0] + list(range(2, len(outputs.get_shape()))))
    outputs = tf.transpose(outputs, axes)
    return (last_output, outputs, new_states)
