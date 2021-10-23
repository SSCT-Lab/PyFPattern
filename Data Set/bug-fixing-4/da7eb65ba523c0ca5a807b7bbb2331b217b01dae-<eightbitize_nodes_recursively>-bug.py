def eightbitize_nodes_recursively(self, current_node):
    'The entry point for transforming a graph into full eight bit.'
    for input_node_name in current_node.input:
        input_node_name = node_name_from_input(input_node_name)
        if (input_node_name in self.already_visited):
            continue
        input_node = self.nodes_map[input_node_name]
        self.eightbitize_nodes_recursively(input_node)
    self.already_visited[current_node.name] = True
    if (current_node.op == 'MatMul'):
        self.eightbitize_mat_mul_node(current_node)
    elif (current_node.op == 'Conv2D'):
        self.eightbitize_conv_node(current_node)
        self.layers_eightbitized.append(current_node.name)
    elif (current_node.op == 'BiasAdd'):
        self.eightbitize_bias_add_node(current_node)
    elif ((current_node.op == 'MaxPool') or (current_node.op == 'AvgPool')):
        self.eightbitize_single_input_tensor_node(current_node, self.add_pool_function)
    elif ((current_node.op == 'Relu') or (current_node.op == 'Relu6')):
        self.eightbitize_single_input_tensor_node(current_node, self.add_relu_function)
    elif (current_node.op == 'Concat'):
        self.eightbitize_concat_node(current_node)
    elif (current_node.op == 'BatchNormWithGlobalNormalization'):
        self.eightbitize_batch_norm_node(current_node)
    else:
        new_node = tf.NodeDef()
        new_node.CopyFrom(current_node)
        self.add_output_graph_node(new_node)