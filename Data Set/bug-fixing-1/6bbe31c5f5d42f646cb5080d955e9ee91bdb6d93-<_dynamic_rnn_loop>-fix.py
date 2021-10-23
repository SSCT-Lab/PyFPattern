

def _dynamic_rnn_loop(cell, inputs, initial_state, parallel_iterations, swap_memory, sequence_length=None, dtype=None):
    'Internal implementation of Dynamic RNN.\n\n  Args:\n    cell: An instance of RNNCell.\n    inputs: A `Tensor` of shape [time, batch_size, input_size], or a nested\n      tuple of such elements.\n    initial_state: A `Tensor` of shape `[batch_size, state_size]`, or if\n      `cell.state_size` is a tuple, then this should be a tuple of\n      tensors having shapes `[batch_size, s] for s in cell.state_size`.\n    parallel_iterations: Positive Python int.\n    swap_memory: A Python boolean\n    sequence_length: (optional) An `int32` `Tensor` of shape [batch_size].\n    dtype: (optional) Expected dtype of output. If not specified, inferred from\n      initial_state.\n\n  Returns:\n    Tuple `(final_outputs, final_state)`.\n    final_outputs:\n      A `Tensor` of shape `[time, batch_size, cell.output_size]`.  If\n      `cell.output_size` is a (possibly nested) tuple of ints or `TensorShape`\n      objects, then this returns a (possibly nested) tuple of Tensors matching\n      the corresponding shapes.\n    final_state:\n      A `Tensor`, or possibly nested tuple of Tensors, matching in length\n      and shapes to `initial_state`.\n\n  Raises:\n    ValueError: If the input depth cannot be inferred via shape inference\n      from the inputs.\n    ValueError: If time_step is not the same for all the elements in the\n      inputs.\n    ValueError: If batch_size is not the same for all the elements in the\n      inputs.\n  '
    state = initial_state
    assert isinstance(parallel_iterations, int), 'parallel_iterations must be int'
    state_size = cell.state_size
    flat_input = nest.flatten(inputs)
    flat_output_size = nest.flatten(cell.output_size)
    input_shape = array_ops.shape(flat_input[0])
    time_steps = input_shape[0]
    batch_size = _best_effort_input_batch_size(flat_input)
    inputs_got_shape = tuple((input_.get_shape().with_rank_at_least(3) for input_ in flat_input))
    (const_time_steps, const_batch_size) = inputs_got_shape[0].as_list()[:2]
    for shape in inputs_got_shape:
        if (not shape[2:].is_fully_defined()):
            raise ValueError('Input size (depth of inputs) must be accessible via shape inference, but saw value None.')
        got_time_steps = shape[0].value
        got_batch_size = shape[1].value
        if (const_time_steps != got_time_steps):
            raise ValueError('Time steps is not the same for all the elements in the input in a batch.')
        if (const_batch_size != got_batch_size):
            raise ValueError('Batch_size is not the same for all the elements in the input.')

    def _create_zero_arrays(size):
        size = _concat(batch_size, size)
        return array_ops.zeros(array_ops.stack(size), _infer_state_dtype(dtype, state))
    flat_zero_output = tuple((_create_zero_arrays(output) for output in flat_output_size))
    zero_output = nest.pack_sequence_as(structure=cell.output_size, flat_sequence=flat_zero_output)
    if (sequence_length is not None):
        min_sequence_length = math_ops.reduce_min(sequence_length)
        max_sequence_length = math_ops.reduce_max(sequence_length)
    else:
        max_sequence_length = time_steps
    time = array_ops.constant(0, dtype=dtypes.int32, name='time')
    with ops.name_scope('dynamic_rnn') as scope:
        base_name = scope

    def _create_ta(name, element_shape, dtype):
        return tensor_array_ops.TensorArray(dtype=dtype, size=time_steps, element_shape=element_shape, tensor_array_name=(base_name + name))
    in_graph_mode = (not context.executing_eagerly())
    if in_graph_mode:
        output_ta = tuple((_create_ta(('output_%d' % i), element_shape=tensor_shape.TensorShape([const_batch_size]).concatenate(_maybe_tensor_shape_from_tensor(out_size)), dtype=_infer_state_dtype(dtype, state)) for (i, out_size) in enumerate(flat_output_size)))
        input_ta = tuple((_create_ta(('input_%d' % i), element_shape=flat_input_i.shape[1:], dtype=flat_input_i.dtype) for (i, flat_input_i) in enumerate(flat_input)))
        input_ta = tuple((ta.unstack(input_) for (ta, input_) in zip(input_ta, flat_input)))
    else:
        output_ta = tuple(([0 for _ in range(time_steps.numpy())] for i in range(len(flat_output_size))))
        input_ta = flat_input

    def _time_step(time, output_ta_t, state):
        'Take a time step of the dynamic RNN.\n\n    Args:\n      time: int32 scalar Tensor.\n      output_ta_t: List of `TensorArray`s that represent the output.\n      state: nested tuple of vector tensors that represent the state.\n\n    Returns:\n      The tuple (time + 1, output_ta_t with updated flow, new_state).\n    '
        if in_graph_mode:
            input_t = tuple((ta.read(time) for ta in input_ta))
            for (input_, shape) in zip(input_t, inputs_got_shape):
                input_.set_shape(shape[1:])
        else:
            input_t = tuple((ta[time.numpy()] for ta in input_ta))
        input_t = nest.pack_sequence_as(structure=inputs, flat_sequence=input_t)
        is_keras_rnn_cell = _is_keras_rnn_cell(cell)
        if (is_keras_rnn_cell and (not nest.is_sequence(state))):
            state = [state]
        call_cell = (lambda : cell(input_t, state))
        if (sequence_length is not None):
            (output, new_state) = _rnn_step(time=time, sequence_length=sequence_length, min_sequence_length=min_sequence_length, max_sequence_length=max_sequence_length, zero_output=zero_output, state=state, call_cell=call_cell, state_size=state_size, skip_conditionals=True)
        else:
            (output, new_state) = call_cell()
        if (is_keras_rnn_cell and (len(new_state) == 1)):
            new_state = new_state[0]
        output = nest.flatten(output)
        if in_graph_mode:
            output_ta_t = tuple((ta.write(time, out) for (ta, out) in zip(output_ta_t, output)))
        else:
            for (ta, out) in zip(output_ta_t, output):
                ta[time.numpy()] = out
        return ((time + 1), output_ta_t, new_state)
    if in_graph_mode:
        loop_bound = math_ops.minimum(time_steps, math_ops.maximum(1, max_sequence_length))
    else:
        loop_bound = time_steps
    (_, output_final_ta, final_state) = control_flow_ops.while_loop(cond=(lambda time, *_: (time < loop_bound)), body=_time_step, loop_vars=(time, output_ta, state), parallel_iterations=parallel_iterations, maximum_iterations=time_steps, swap_memory=swap_memory)
    if in_graph_mode:
        final_outputs = tuple((ta.stack() for ta in output_final_ta))
        for (output, output_size) in zip(final_outputs, flat_output_size):
            shape = _concat([const_time_steps, const_batch_size], output_size, static=True)
            output.set_shape(shape)
    else:
        final_outputs = output_final_ta
    final_outputs = nest.pack_sequence_as(structure=cell.output_size, flat_sequence=final_outputs)
    if (not in_graph_mode):
        final_outputs = nest.map_structure_up_to(cell.output_size, (lambda x: array_ops.stack(x, axis=0)), final_outputs)
    return (final_outputs, final_state)
