def print_input_nodes(current_node, nodes_map, indent, already_visited):
    print(((((' ' * indent) + current_node.op) + ':') + current_node.name))
    for input_node_name in current_node.input:
        if (input_node_name in already_visited):
            continue
        input_node = nodes_map[input_node_name]
        print_input_nodes(input_node, nodes_map, (indent + 1), already_visited)
    already_visited[current_node.name] = True