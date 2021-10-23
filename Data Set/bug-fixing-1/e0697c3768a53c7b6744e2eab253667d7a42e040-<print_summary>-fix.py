

def print_summary(model, line_length=None, positions=None):
    'Prints a summary of a model.\n\n    # Arguments\n        model: Keras model instance.\n        line_length: total length of printed lines\n        positions: relative or absolute positions of log elements in each line.\n            If not provided, defaults to `[.33, .55, .67, 1.]`.\n    '
    if (model.__class__.__name__ == 'Sequential'):
        sequential_like = True
    else:
        sequential_like = True
        for v in model.nodes_by_depth.values():
            if (len(v) > 1):
                sequential_like = False
                break
    if sequential_like:
        line_length = (line_length or 65)
        positions = (positions or [0.45, 0.85, 1.0])
        if (positions[(- 1)] <= 1):
            positions = [int((line_length * p)) for p in positions]
        to_display = ['Layer (type)', 'Output Shape', 'Param #']
    else:
        line_length = (line_length or 100)
        positions = (positions or [0.33, 0.55, 0.67, 1.0])
        if (positions[(- 1)] <= 1):
            positions = [int((line_length * p)) for p in positions]
        to_display = ['Layer (type)', 'Output Shape', 'Param #', 'Connected to']
        relevant_nodes = []
        for v in model.nodes_by_depth.values():
            relevant_nodes += v

    def print_row(fields, positions):
        line = ''
        for i in range(len(fields)):
            if (i > 0):
                line = (line[:(- 1)] + ' ')
            line += str(fields[i])
            line = line[:positions[i]]
            line += (' ' * (positions[i] - len(line)))
        print(line)
    print(('_' * line_length))
    print_row(to_display, positions)
    print(('=' * line_length))

    def print_layer_summary(layer):
        try:
            output_shape = layer.output_shape
        except AttributeError:
            output_shape = 'multiple'
        name = layer.name
        cls_name = layer.__class__.__name__
        fields = [(((name + ' (') + cls_name) + ')'), output_shape, layer.count_params()]
        print_row(fields, positions)

    def print_layer_summary_with_connections(layer):
        'Prints a summary for a single layer.\n\n        # Arguments\n            layer: target layer.\n        '
        try:
            output_shape = layer.output_shape
        except AttributeError:
            output_shape = 'multiple'
        connections = []
        for node in layer.inbound_nodes:
            if (relevant_nodes and (node not in relevant_nodes)):
                continue
            for i in range(len(node.inbound_layers)):
                inbound_layer = node.inbound_layers[i].name
                inbound_node_index = node.node_indices[i]
                inbound_tensor_index = node.tensor_indices[i]
                connections.append((((((inbound_layer + '[') + str(inbound_node_index)) + '][') + str(inbound_tensor_index)) + ']'))
        name = layer.name
        cls_name = layer.__class__.__name__
        if (not connections):
            first_connection = ''
        else:
            first_connection = connections[0]
        fields = [(((name + ' (') + cls_name) + ')'), output_shape, layer.count_params(), first_connection]
        print_row(fields, positions)
        if (len(connections) > 1):
            for i in range(1, len(connections)):
                fields = ['', '', '', connections[i]]
                print_row(fields, positions)
    layers = model.layers
    for i in range(len(layers)):
        if sequential_like:
            print_layer_summary(layers[i])
        else:
            print_layer_summary_with_connections(layers[i])
        if (i == (len(layers) - 1)):
            print(('=' * line_length))
        else:
            print(('_' * line_length))
    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))
    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))
    print('Total params: {:,}'.format((trainable_count + non_trainable_count)))
    print('Trainable params: {:,}'.format(trainable_count))
    print('Non-trainable params: {:,}'.format(non_trainable_count))
    print(('_' * line_length))
