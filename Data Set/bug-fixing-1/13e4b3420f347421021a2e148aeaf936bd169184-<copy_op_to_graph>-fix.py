

def copy_op_to_graph(org_instance, to_graph, variables, scope=''):
    'Given an `Operation` `org_instance` from one `Graph`,\n  initializes and returns a copy of it from another `Graph`,\n  under the specified scope (default `""`).\n\n  The copying is done recursively, so any `Operation` whose output\n  is required to evaluate the `org_instance`, is also copied (unless\n  already done).\n\n  Since `Variable` instances are copied separately, those required\n  to evaluate `org_instance` must be provided as input.\n\n  Args:\n    org_instance: An `Operation` from some `Graph`. Could be a\n      `Placeholder` as well.\n    to_graph: The `Graph` to copy `org_instance` to.\n    variables: An iterable of `Variable` instances to copy `org_instance` to.\n    scope: A scope for the new `Variable` (default `""`).\n\n  Returns:\n    The copied `Operation` from `to_graph`.\n\n  Raises:\n    TypeError: If `org_instance` is not an `Operation` or `Tensor`.\n  '
    if (scope != ''):
        new_name = ((scope + '/') + org_instance.name)
    else:
        new_name = org_instance.name
    copied_variables = dict(((x.name, x) for x in variables))
    if (new_name in copied_variables):
        return to_graph.get_tensor_by_name(copied_variables[new_name].name)
    try:
        already_present = to_graph.as_graph_element(new_name, allow_tensor=True, allow_operation=True)
        return already_present
    except:
        pass
    collections = []
    for (name, collection) in org_instance.graph._collections.items():
        if (org_instance in collection):
            if (scope == ''):
                collections.append(name)
            else:
                collections.append(((scope + '/') + name))
    if isinstance(org_instance, ops.Tensor):
        op = org_instance.op
        new_op = copy_op_to_graph(op, to_graph, variables, scope)
        output_index = op.outputs.index(org_instance)
        new_tensor = new_op.outputs[output_index]
        for collection in collections:
            to_graph.add_to_collection(collection, new_tensor)
        return new_tensor
    elif isinstance(org_instance, ops.Operation):
        op = org_instance
        if (op._original_op is not None):
            new_original_op = copy_op_to_graph(op._original_op, to_graph, variables, scope)
        else:
            new_original_op = None
        new_control_inputs = [copy_op_to_graph(x, to_graph, variables, scope) for x in op.control_inputs]
        new_inputs = [copy_op_to_graph(x, to_graph, variables, scope) for x in op.inputs]
        new_node_def = deepcopy(op._node_def)
        new_node_def.name = new_name
        output_types = op._output_types[:]
        input_types = op._input_types[:]
        op_def = deepcopy(op._op_def)
        new_op = ops.Operation(new_node_def, to_graph, new_inputs, output_types, new_control_inputs, input_types, new_original_op, op_def)
        to_graph._add_op(new_op)
        to_graph._record_op_seen_by_control_dependencies(new_op)
        for device_function in reversed(to_graph._device_function_stack):
            new_op._set_device(device_function(new_op))
        return new_op
    else:
        raise TypeError(('Could not copy instance: ' + str(org_instance)))
