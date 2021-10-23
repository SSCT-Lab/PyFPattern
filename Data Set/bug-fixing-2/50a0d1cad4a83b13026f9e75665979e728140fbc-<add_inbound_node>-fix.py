

def add_inbound_node(self, inbound_layers, node_indices=None, tensor_indices=None):
    '\n        # Arguments:\n            inbound_layers: can be a layer instance\n                or a list/tuple of layer instances.\n            node_indices: integer (or list of integers).\n                The input layer might have a number of\n                parallel output streams;\n                this is the index of the stream (in the input layer)\n                where to connect the current layer.\n            tensor_indices: integer or list of integers.\n                The output of the inbound node might be a list/tuple\n                of tensor, and we might only be interested in one sepcific entry.\n                This index allows you to specify the index of the entry in the output list\n                (if applicable). "None" means that we take all outputs (as a list).\n        '
    inbound_layers = to_list(inbound_layers)
    if (not node_indices):
        node_indices = [0 for _ in range(len(inbound_layers))]
    else:
        node_indices = to_list(node_indices)
        assert (len(node_indices) == len(inbound_layers))
    if (not tensor_indices):
        tensor_indices = [0 for _ in range(len(inbound_layers))]
    else:
        tensor_indices = to_list(tensor_indices)
    if (not self.built):
        input_shapes = []
        for (layer, node_index, tensor_index) in zip(inbound_layers, node_indices, tensor_indices):
            input_shapes.append(layer.inbound_nodes[node_index].output_shapes[tensor_index])
        if (len(input_shapes) == 1):
            self.build(input_shape=input_shapes[0])
        else:
            self.build(input_shape=input_shapes)
        self.built = True
    Node.create_node(self, inbound_layers, node_indices, tensor_indices)
