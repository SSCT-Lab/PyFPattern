

def _copy_non_source(op, graph, op_map):
    "Copy an op directly to a given graph.\n\n  Generally `op`'s inputs should already have been copied. If this is not the\n  case, for example with v1 while_loops, then `_copy_non_source` inserts\n  placeholders for the unavailable Tensors and returns a list of required\n  mutations.\n\n  Args:\n    op: The op to be copied.\n    graph: The destination graph.\n    op_map: A dict mapping ops and tensors in the old graph to the new one.\n  Returns:\n    A tuple of (required_inputs, required_control_inputs):\n      required_inputs:\n        A list of `_InputMutation` tuples containing inputs to `copied_op` which\n        must be updated once `old_graph_tensor` has been copied.\n      required_control_inputs:\n        A list of `_ControlMutation` tuples containing control inputs to\n        `copied_op` which must be added once `old_graph_op` has been copied.\n  "
    input_mutations = []
    control_mutations = []
    copied_inputs = []
    for (input_index, original_input) in enumerate(op.inputs):
        copied_input = op_map.get(original_input, None)
        if (copied_input is None):
            copied_input = array_ops.placeholder(name='unused_control_flow_input', shape=original_input.shape, dtype=original_input.dtype)
            input_mutations.append(_InputMutation(copied_op=None, input_index=input_index, old_graph_tensor=original_input))
        copied_inputs.append(copied_input)
    copied_control_inputs = []
    for original_control_input in op.control_inputs:
        copied_control_input = op_map.get(original_control_input, None)
        if (copied_control_input is None):
            control_mutations.append(_ControlMutation(copied_op=None, old_graph_op=original_control_input))
        else:
            copied_control_inputs.append(copied_control_input)
    with ops.control_dependencies(copied_control_inputs), ops.device(op.device):
        copied_op = graph.create_op(op_type=op.type, inputs=copied_inputs, dtypes=[x.dtype for x in op.outputs], attrs=op.node_def.attr, name=op.name)
    op_map[op] = copied_op
    for (i, o) in enumerate(op.outputs):
        op_map[o] = copied_op.outputs[i]
    return ([mutation._replace(copied_op=copied_op) for mutation in input_mutations], [mutation._replace(copied_op=copied_op) for mutation in control_mutations])
