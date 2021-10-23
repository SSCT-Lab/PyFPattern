def model_to_dot(model, show_shapes=False, show_layer_names=True, rankdir='TB', expand_nested=False, dpi=96, subgraph=False):
    "Convert a Keras model to dot format.\n\n    # Arguments\n        model: A Keras model instance.\n        show_shapes: whether to display shape information.\n        show_layer_names: whether to display layer names.\n        rankdir: `rankdir` argument passed to PyDot,\n            a string specifying the format of the plot:\n            'TB' creates a vertical plot;\n            'LR' creates a horizontal plot.\n        expand_nested: whether to expand nested models into clusters.\n        dpi: dot DPI.\n        subgraph: whether to return a pydot.Cluster instance.\n\n    # Returns\n        A `pydot.Dot` instance representing the Keras model or\n        a `pydot.Cluster` instance representing nested model if\n        `subgraph=True`.\n    "
    from ..layers.wrappers import Wrapper
    from ..models import Model
    from ..models import Sequential
    _check_pydot()
    if subgraph:
        dot = pydot.Cluster(style='dashed')
        dot.set('label', model.name)
        dot.set('labeljust', 'l')
    else:
        dot = pydot.Dot()
        dot.set('rankdir', rankdir)
        dot.set('concentrate', True)
        dot.set('dpi', dpi)
        dot.set_node_defaults(shape='record')
    if isinstance(model, Sequential):
        if (not model.built):
            model.build()
    layers = model._layers
    for (i, layer) in enumerate(layers):
        layer_id = str(id(layer))
        layer_name = layer.name
        class_name = layer.__class__.__name__
        if isinstance(layer, Wrapper):
            if (expand_nested and isinstance(layer.layer, Model)):
                submodel = model_to_dot(layer.layer, show_shapes, show_layer_names, rankdir, expand_nested, subgraph=True)
                model_nodes = submodel.get_nodes()
                dot.add_edge(pydot.Edge(layer_id, model_nodes[0].get_name()))
                if (len(layers) > (i + 1)):
                    next_layer_id = str(id(layers[(i + 1)]))
                    dot.add_edge(pydot.Edge(model_nodes[(len(model_nodes) - 1)].get_name(), next_layer_id))
                dot.add_subgraph(submodel)
            else:
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
                    if ((not expand_nested) or (not (isinstance(inbound_layer, Wrapper) and isinstance(inbound_layer.layer, Model)))):
                        inbound_layer_id = str(id(inbound_layer))
                        assert dot.get_node(inbound_layer_id)
                        assert dot.get_node(layer_id)
                        dot.add_edge(pydot.Edge(inbound_layer_id, layer_id))
    return dot