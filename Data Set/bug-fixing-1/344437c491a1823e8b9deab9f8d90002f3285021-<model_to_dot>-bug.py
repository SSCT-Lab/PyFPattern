

def model_to_dot(model, show_shapes=False):
    dot = pydot.Dot()
    dot.set('rankdir', 'TB')
    dot.set('concentrate', True)
    dot.set_node_defaults(shape='record')
    if (model.__class__.__name__ == 'Sequential'):
        if (not model.built):
            model.build()
        model = model.model
    layers = model.layers
    for layer in layers:
        layer_id = str(id(layer))
        label = (((str(layer.name) + ' (') + layer.__class__.__name__) + ')')
        if show_shapes:
            outputlabels = str(layer.output_shape)
            if hasattr(layer, 'input_shape'):
                inputlabels = str(layer.input_shape)
            elif hasattr(layer, 'input_shapes'):
                inputlabels = ', '.join([str(ishape) for ishape in layer.input_shapes])
            else:
                inputlabels = ''
            label = ('%s\n|{input:|output:}|{{%s}|{%s}}' % (label, inputlabels, outputlabels))
        node = pydot.Node(layer_id, label=label)
        dot.add_node(node)
    for layer in layers:
        layer_id = str(id(layer))
        for (i, node) in enumerate(layer.inbound_nodes):
            node_key = ((layer.name + '_ib-') + str(i))
            if (node_key in model.container_nodes):
                for inbound_layer in node.inbound_layers:
                    inbound_layer_id = str(id(inbound_layer))
                    layer_id = str(id(layer))
                    dot.add_edge(pydot.Edge(inbound_layer_id, layer_id))
    return dot
