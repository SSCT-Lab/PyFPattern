def round_nodes_recursively(self, current_node):
    'The entry point for simple rounding quantization.'
    self.already_visited[current_node.name] = True
    for input_node_name in current_node.input:
        input_node_name = node_name_from_input(input_node_name)
        if (input_node_name in self.already_visited):
            continue
        input_node = self.nodes_map[input_node_name]
        self.round_nodes_recursively(input_node)
    nodes_to_quantize = ['Conv2D', 'BiasAdd', 'MatMul']
    if any(((current_node.op in s) for s in nodes_to_quantize)):
        new_node = tf.NodeDef()
        new_node.CopyFrom(current_node)
        new_node.name = (current_node.name + '_original')
        self.add_output_graph_node(new_node)
        levels = (1 << FLAGS.bitdepth)
        constant_name = (current_node.name + '_round_depth')
        constant_tensor = tf.constant(levels, dtype=tf.int32, name=constant_name)
        constant_node = constant_tensor.op.node_def
        self.add_output_graph_node(constant_node)
        quantize_node = tf.NodeDef()
        quantize_node.op = 'RoundToSteps'
        quantize_node.name = current_node.name
        quantize_node.input.extend([(current_node.name + '_original')])
        quantize_node.input.extend([constant_node.name])
        self.add_output_graph_node(quantize_node)
    else:
        new_node = tf.NodeDef()
        new_node.CopyFrom(current_node)
        self.add_output_graph_node(new_node)