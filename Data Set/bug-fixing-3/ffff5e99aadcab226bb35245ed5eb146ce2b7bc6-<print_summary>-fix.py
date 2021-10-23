def print_summary(layers, relevant_nodes=None, line_length=100, positions=[0.33, 0.55, 0.67, 1.0]):
    if (positions[(- 1)] <= 1):
        positions = [int((line_length * p)) for p in positions]
    to_display = ['Layer (type)', 'Output Shape', 'Param #', 'Connected to']

    def print_row(fields, positions):
        line = ''
        for i in range(len(fields)):
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
        except:
            output_shape = 'multiple'
        connections = []
        for (node_index, node) in enumerate(layer.inbound_nodes):
            if relevant_nodes:
                node_key = ((layer.name + '_ib-') + str(node_index))
                if (node_key not in relevant_nodes):
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
    for i in range(len(layers)):
        print_layer_summary(layers[i])
        if (i == (len(layers) - 1)):
            print(('=' * line_length))
        else:
            print(('_' * line_length))

    def count_total_params(layers, layer_set=None):
        if (layer_set is None):
            layer_set = set()
        total_params = 0
        for layer in layers:
            if (layer in layer_set):
                continue
            layer_set.add(layer)
            if (type(layer) in (Model, Sequential)):
                total_params += count_total_params(layer.layers, layer_set)
            else:
                total_params += layer.count_params()
        return total_params
    print(('Total params: %s' % count_total_params(layers)))
    print(('_' * line_length))