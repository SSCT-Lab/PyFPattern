def quantize_nodes_recursively(self, current_node):
    'The entry point for quantizing nodes to eight bit and back.'
    for input_node_name in current_node.input:
        input_node_name = node_name_from_input(input_node_name)
        if (input_node_name in self.already_visited):
            continue
        input_node = self.nodes_map[input_node_name]
        self.quantize_nodes_recursively(input_node)
    self.already_visited[current_node.name] = True
    nodes_to_quantize = ['Conv2D', 'BiasAdd', 'MatMul']
    if any(((current_node.op in s) for s in nodes_to_quantize)):
        for input_name in current_node.input:
            input_name = node_name_from_input(input_name)
            input_node = self.nodes_map[input_name]
            self.quantize_node(input_node)
        self.quantize_node(current_node)
    else:
        new_node = tf.NodeDef()
        new_node.CopyFrom(current_node)
        self.add_output_graph_node(new_node)