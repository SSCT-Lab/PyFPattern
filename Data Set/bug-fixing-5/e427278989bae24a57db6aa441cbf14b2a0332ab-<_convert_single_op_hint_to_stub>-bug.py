def _convert_single_op_hint_to_stub(call, graph_def, function_def_nodes=None, is_last_run=True):
    'Given a graph_def, converts `call` into a stub and returns a new graph_def.\n\n  Args:\n    call: A single function call to be converted.\n    graph_def: A graph_def to use as input (that hass call obviously).\n    function_def_nodes: Nodes inside the function def those are not connected to\n      the graph.\n    is_last_run: Whether it is the last run for a given pass (for OpHint has\n      children).\n\n  Returns:\n    A new transformed graph-def that has call as a stub (single op).\n\n  Note: after this process, the graph_def can no longer be loaded into\n      the tensorflow runtime, so all future manipulations are done in graph_def\n      level.\n  '
    if (function_def_nodes is None):
        function_def_nodes = set()
    (name_to_input_name, name_to_node, name_to_seq_num) = _extract_graph_summary(graph_def)
    (input_names, output_names) = call.flattened_inputs_and_outputs()
    reachable_by_input = _bfs_for_reachable_nodes(input_names, name_to_input_name)
    reachable_by_output = _bfs_for_reachable_nodes(output_names, name_to_input_name)
    output_nodes_set = set(output_names)
    nodes_after_fuse = []
    nodes_deleted_by_fuse = set()
    for node in graph_def.node:
        n = _tensor_name_base(node.name)
        if (n in reachable_by_output):
            if ((n not in reachable_by_input) and (n not in output_nodes_set)):
                nodes_deleted_by_fuse.add(n)
        elif ((n not in reachable_by_input) and (n not in function_def_nodes)):
            nodes_after_fuse.append(n)
        elif (not is_last_run):
            nodes_after_fuse.append(n)
    out = _graph_pb2.GraphDef()
    reachable_by_input_sorted = sorted(list(reachable_by_input), key=(lambda n: name_to_seq_num[n]))
    for node in reachable_by_input_sorted:
        out.node.extend([_copy.deepcopy(name_to_node[node])])
    sorted_input_indices = list(call.inputs.keys())
    sorted_input_indices.sort()
    sorted_output_indices = list(call.outputs.keys())
    sorted_output_indices.sort()
    new_node = _node_def_pb2.NodeDef()
    for input_index in sorted_input_indices:
        inputs = call.inputs[input_index]
        input_name = inputs.aggregate_and_return_name_for_input(out)
        new_node.input.append(input_name)
    new_node.attr[OpHint.TFLITE_INPUT_INDICES].list.i.extend(sorted_input_indices)
    new_node.op = call.function_name
    new_node.name = call.uuid
    out.node.extend([new_node])
    output_dtypes = []
    for output_index in sorted_output_indices:
        output = call.outputs[output_index]
        output_dtype = output.aggregate_and_return_name_for_output(new_node.name, output_index, out)
        output_dtypes.append(output_dtype)
    new_node.attr['_output_types'].list.type[:] = output_dtypes
    new_node.attr['_output_quantized'].b = False
    for n in nodes_after_fuse:
        should_keep = True
        for input_name in name_to_input_name[n]:
            if (input_name in nodes_deleted_by_fuse):
                should_keep = False
        if should_keep:
            out.node.extend([_copy.deepcopy(name_to_node[n])])
    out.library.CopyFrom(graph_def.library)
    out.versions.CopyFrom(graph_def.versions)
    return out