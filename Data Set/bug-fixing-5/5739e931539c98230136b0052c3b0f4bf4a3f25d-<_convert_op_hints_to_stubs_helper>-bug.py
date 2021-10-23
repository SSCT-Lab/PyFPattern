def _convert_op_hints_to_stubs_helper(graph_def, write_callback=(lambda sess, graph_def: None)):
    'Converts a graph_def to a new graph_def where all op hints are stubbed.\n\n  Args:\n    graph_def: A graph def that we should convert.\n    write_callback: A function pointer that can be used to write intermediate\n      steps of graph transformation (optional).\n  Returns:\n    A new stubbed graph_def.\n  '
    hints = _find_all_hints_in_nodes(graph_def.node)
    hints_q = []
    for hint in _six.itervalues(hints):
        hints_q.append((hint.level, hint.uuid))
    hints_q.sort(key=(lambda tup: tup[0]))
    for i in range((len(hints_q) - 1), (- 1), (- 1)):
        (level, hint_uuid) = hints_q[i]
    curr_graph_def = graph_def
    del graph_def
    for i in range((len(hints_q) - 1), (- 1), (- 1)):
        (level, hint_uuid) = hints_q[i]
        if (level >= 2):
            (children_hints, curr_graph_def, function_def_nodes) = _find_children_hints(hints[hint_uuid], curr_graph_def)
            assert (len(children_hints) > 0)
            children_inputs_mappings = hints[hint_uuid].children_inputs_mappings
            for j in range(len(children_hints)):
                child_hint = children_hints[j]
                if (j == 0):
                    for mapping in children_inputs_mappings['parent_first_child_input']:
                        parent_input_index = _get_correct_mapping(mapping['parent_ophint_input_index'], hints[hint_uuid].inputs)
                        child_input_index = _get_correct_mapping(mapping['first_child_ophint_input_index'], child_hint.inputs)
                        child_hint.inputs[child_input_index] = hints[hint_uuid].inputs[parent_input_index]
                else:
                    for mapping in children_inputs_mappings['internal_children_input_output']:
                        input_index = _get_correct_mapping(mapping['child_input_index'], child_hint.inputs)
                        output_index = _get_correct_mapping(mapping['child_output_index'], children_hints[(j - 1)].outputs)
                        child_hint.inputs[input_index] = children_hints[(j - 1)].outputs[output_index]
                if (j == (len(children_hints) - 1)):
                    for mapping in children_inputs_mappings['parent_last_child_output']:
                        parent_output_index = _get_correct_mapping(mapping['parent_output_index'], hints[hint_uuid].outputs)
                        child_output_index = _get_correct_mapping(mapping['child_output_index'], child_hint.outputs)
                        child_hint.outputs[child_output_index] = hints[hint_uuid].outputs[parent_output_index]
            for j in range(len(children_hints)):
                child_hint = children_hints[j]
                curr_graph_def = _convert_single_op_hint_to_stub(child_hint, curr_graph_def, function_def_nodes, (j == (len(children_hints) - 1)))
        else:
            curr_graph_def = _convert_single_op_hint_to_stub(hints[hint_uuid], curr_graph_def)
            write_callback(curr_graph_def, 'initial')
    curr_graph_def = _remove_redundant_stack_unstack(curr_graph_def)
    return curr_graph_def