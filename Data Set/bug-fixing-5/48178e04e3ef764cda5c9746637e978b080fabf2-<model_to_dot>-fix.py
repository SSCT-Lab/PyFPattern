def model_to_dot(model, show_shapes=False, show_layer_names=True, rankdir='TB'):
    "Convert a Keras model to dot format.\n\n  Arguments:\n      model: A Keras model instance.\n      show_shapes: whether to display shape information.\n      show_layer_names: whether to display layer names.\n      rankdir: `rankdir` argument passed to PyDot,\n          a string specifying the format of the plot:\n          'TB' creates a vertical plot;\n          'LR' creates a horizontal plot.\n\n  Returns:\n      A `pydot.Dot` instance representing the Keras model.\n  "
    from tensorflow.python.keras._impl.keras.layers.wrappers import Wrapper
    from tensorflow.python.keras._impl.keras.models import Sequential
    _check_pydot()
    dot = pydot.Dot()
    dot.set('rankdir', rankdir)
    dot.set('concentrate', True)
    dot.set_node_defaults(shape='record')
    if isinstance(model, Sequential):
        if (not model.built):
            model.build()
        model = model.model
    layers = model.layers
    for layer in layers:
        layer_id = str(id(layer))
        layer_name = layer.name
        class_name = layer.__class__.__name__
        if isinstance(layer, Wrapper):
            layer_name = '{}({})'.format(layer_name, layer.layer.name)
            child_class_name = layer.layer.__class__.__name__
            class_name = '{}({})'.format(class_name, child_class_name)
        if show_layer_names:
            label = '{}: {}'.format(layer_name, class_name)
        else:
            label = class_name
        if show_shapes:
            try:
                outputlabels = str(layer.output_shape)
            except AttributeError:
                outputlabels = 'multiple'
            if hasattr(layer, 'input_shape'):
                inputlabels = str(layer.input_shape)
            elif hasattr(layer, 'input_shapes'):
                inputlabels = ', '.join([str(ishape) for ishape in layer.input_shapes])
            else:
                inputlabels = 'multiple'
            label = ('%s\n|{input:|output:}|{{%s}|{%s}}' % (label, inputlabels, outputlabels))
        node = pydot.Node(layer_id, label=label)
        dot.add_node(node)
    for layer in layers:
        layer_id = str(id(layer))
        for (i, node) in enumerate(layer._inbound_nodes):
            node_key = ((layer.name + '_ib-') + str(i))
            if (node_key in model._network_nodes):
                for inbound_layer in node.inbound_layers:
                    inbound_layer_id = str(id(inbound_layer))
                    layer_id = str(id(layer))
                    dot.add_edge(pydot.Edge(inbound_layer_id, layer_id))
    return dot