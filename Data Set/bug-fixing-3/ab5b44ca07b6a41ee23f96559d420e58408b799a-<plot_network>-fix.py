def plot_network(symbol, title='plot', save_format='pdf', shape=None, dtype=None, node_attrs={
    
}, hide_weights=True):
    'Creates a visualization (Graphviz digraph object) of the given computation graph.\n    Graphviz must be installed for this function to work.\n\n    Parameters\n    ----------\n    title: str, optional\n        Title of the generated visualization.\n    symbol: Symbol\n        A symbol from the computation graph. The generated digraph will visualize the part\n        of the computation graph required to compute `symbol`.\n    shape: dict, optional\n        Specifies the shape of the input tensors. If specified, the visualization will include\n        the shape of the tensors between the nodes. `shape` is a dictionary mapping\n        input symbol names (str) to the corresponding tensor shape (tuple).\n    dtype: dict, optional\n        Specifies the type of the input tensors. If specified, the visualization will include\n        the type of the tensors between the nodes. `dtype` is a dictionary mapping\n        input symbol names (str) to the corresponding tensor type (e.g. `numpy.float32`).\n    node_attrs: dict, optional\n        Specifies the attributes for nodes in the generated visualization. `node_attrs` is\n        a dictionary of Graphviz attribute names and values. For example::\n\n            node_attrs={"shape":"oval","fixedsize":"false"}\n\n        will use oval shape for nodes and allow variable sized nodes in the visualization.\n    hide_weights: bool, optional\n        If True (default), then inputs with names of form *_weight* (corresponding to weight\n        tensors) or *_bias* (corresponding to bias vectors) will be hidden for a cleaner\n        visualization.\n\n    Returns\n    -------\n    dot: Digraph\n        A Graphviz digraph object visualizing the computation graph to compute `symbol`.\n\n    Example\n    -------\n    >>> net = mx.sym.Variable(\'data\')\n    >>> net = mx.sym.FullyConnected(data=net, name=\'fc1\', num_hidden=128)\n    >>> net = mx.sym.Activation(data=net, name=\'relu1\', act_type="relu")\n    >>> net = mx.sym.FullyConnected(data=net, name=\'fc2\', num_hidden=10)\n    >>> net = mx.sym.SoftmaxOutput(data=net, name=\'out\')\n    >>> digraph = mx.viz.plot_network(net, shape={\'data\':(100,200)},\n    ... node_attrs={"fixedsize":"false"})\n    >>> digraph.view()\n\n    Notes\n    -----\n    If ``mxnet`` is imported, the visualization module can be used in its short-form.\n    For example, if we ``import mxnet`` as follows::\n\n        import mxnet\n\n    this method in visualization module can be used in its short-form as::\n\n        mxnet.viz.plot_network(...)\n\n    '
    try:
        from graphviz import Digraph
    except:
        raise ImportError('Draw network requires graphviz library')
    if (not isinstance(symbol, Symbol)):
        raise TypeError('symbol must be a Symbol')
    internals = symbol.get_internals()
    draw_shape = (shape is not None)
    if draw_shape:
        (_, out_shapes, _) = internals.infer_shape(**shape)
        if (out_shapes is None):
            raise ValueError('Input shape is incomplete')
        shape_dict = dict(zip(internals.list_outputs(), out_shapes))
    draw_type = (dtype is not None)
    if draw_type:
        (_, out_types, _) = internals.infer_type(**dtype)
        if (out_types is None):
            raise ValueError('Input type is incomplete')
        type_dict = dict(zip(internals.list_outputs(), out_types))
    conf = json.loads(symbol.tojson())
    nodes = conf['nodes']
    if (len(nodes) != len(set([node['name'] for node in nodes]))):
        seen_nodes = set()
        repeated = set((node['name'] for node in nodes if ((node['name'] in seen_nodes) or seen_nodes.add(node['name']))))
        warning_message = ('There are multiple variables with the same name in your graph, this may result in cyclic graph. Repeated names: ' + ','.join(repeated))
        warnings.warn(warning_message, RuntimeWarning)
    node_attr = {
        'shape': 'box',
        'fixedsize': 'true',
        'width': '1.3',
        'height': '0.8034',
        'style': 'filled',
    }
    node_attr.update(node_attrs)
    dot = Digraph(name=title, format=save_format)
    cm = ('#8dd3c7', '#fb8072', '#ffffb3', '#bebada', '#80b1d3', '#fdb462', '#b3de69', '#fccde5')

    def looks_like_weight(name):
        'Internal helper to figure out if node should be hidden with `hide_weights`.\n        '
        weight_like = ('_weight', '_bias', '_beta', '_gamma', '_moving_var', '_moving_mean', '_running_var', '_running_mean')
        return name.endswith(weight_like)
    hidden_nodes = set()
    for node in nodes:
        op = node['op']
        name = node['name']
        attr = copy.deepcopy(node_attr)
        label = name
        if (op == 'null'):
            if looks_like_weight(node['name']):
                if hide_weights:
                    hidden_nodes.add(node['name'])
                continue
            attr['shape'] = 'oval'
            label = node['name']
            attr['fillcolor'] = cm[0]
        elif (op == 'Convolution'):
            label = 'Convolution\n{kernel}/{stride}, {filter}'.format(kernel='x'.join(_str2tuple(node['attrs']['kernel'])), stride=('x'.join(_str2tuple(node['attrs']['stride'])) if ('stride' in node['attrs']) else '1'), filter=node['attrs']['num_filter'])
            attr['fillcolor'] = cm[1]
        elif (op == 'FullyConnected'):
            label = 'FullyConnected\n{hidden}'.format(hidden=node['attrs']['num_hidden'])
            attr['fillcolor'] = cm[1]
        elif (op == 'BatchNorm'):
            attr['fillcolor'] = cm[3]
        elif (op == 'Activation'):
            act_type = node['attrs']['act_type']
            label = 'Activation\n{activation}'.format(activation=act_type)
            attr['fillcolor'] = cm[2]
        elif (op == 'LeakyReLU'):
            attrs = node.get('attrs')
            act_type = (attrs.get('act_type', 'Leaky') if attrs else 'Leaky')
            label = 'LeakyReLU\n{activation}'.format(activation=act_type)
            attr['fillcolor'] = cm[2]
        elif (op == 'Pooling'):
            label = 'Pooling\n{pooltype}, {kernel}/{stride}'.format(pooltype=node['attrs']['pool_type'], kernel=('x'.join(_str2tuple(node['attrs']['kernel'])) if ('kernel' in node['attrs']) else '[]'), stride=('x'.join(_str2tuple(node['attrs']['stride'])) if ('stride' in node['attrs']) else '1'))
            attr['fillcolor'] = cm[4]
        elif (op in ('Concat', 'Flatten', 'Reshape')):
            attr['fillcolor'] = cm[5]
        elif (op == 'Softmax'):
            attr['fillcolor'] = cm[6]
        else:
            attr['fillcolor'] = cm[7]
            if (op == 'Custom'):
                label = node['attrs']['op_type']
        dot.node(name=name, label=label, **attr)
    for node in nodes:
        op = node['op']
        name = node['name']
        if (op == 'null'):
            continue
        else:
            inputs = node['inputs']
            for item in inputs:
                input_node = nodes[item[0]]
                input_name = input_node['name']
                if (input_name not in hidden_nodes):
                    attr = {
                        'dir': 'back',
                        'arrowtail': 'open',
                        'label': '',
                    }
                    if draw_shape:
                        if (input_node['op'] != 'null'):
                            key = (input_name + '_output')
                            if ('attrs' in input_node):
                                params = input_node['attrs']
                                if ('num_outputs' in params):
                                    key += str((int(params['num_outputs']) - 1))
                            shape = shape_dict[key][1:]
                            label = 'x'.join([str(x) for x in shape])
                            attr['label'] = label
                        else:
                            key = input_name
                            shape = shape_dict[key][1:]
                            label = 'x'.join([str(x) for x in shape])
                            attr['label'] = label
                    if draw_type:
                        if (input_node['op'] != 'null'):
                            key = (input_name + '_output')
                            if ('attrs' in input_node):
                                params = input_node['attrs']
                                if ('num_outputs' in params):
                                    key += str((int(params['num_outputs']) - 1))
                            dtype = type_dict[key]
                            attr['label'] += (('(' + dtype.__name__) + ')')
                        else:
                            key = input_name
                            dtype = type_dict[key]
                            attr['label'] += (('(' + dtype.__name__) + ')')
                    dot.edge(tail_name=name, head_name=input_name, **attr)
    return dot