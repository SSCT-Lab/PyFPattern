

def plot_network(symbol, title='plot', save_format='pdf', shape=None, node_attrs={
    
}, hide_weights=True):
    'Creates a visualization (Graphviz digraph object) of the given computation graph.\n    Graphviz must be installed for this function to work.\n\n    Parameters\n    ----------\n    title: str, optional\n        Title of the generated visualization.\n    symbol: Symbol\n        A symbol from the computation graph. The generated digraph will visualize the part\n        of the computation graph required to compute `symbol`.\n    shape: dict, optional\n        Specifies the shape of the input tensors. If specified, the visualization will include\n        the shape of the tensors between the nodes. `shape` is a dictionary mapping\n        input symbol names (str) to the corresponding tensor shape (tuple).\n    node_attrs: dict, optional\n        Specifies the attributes for nodes in the generated visualization. `node_attrs` is\n        a dictionary of Graphviz attribute names and values. For example,\n            ``node_attrs={"shape":"oval","fixedsize":"false"}``\n            will use oval shape for nodes and allow variable sized nodes in the visualization.\n    hide_weights: bool, optional\n        If True (default), then inputs with names of form *_weight (corresponding to weight\n        tensors) or *_bias (corresponding to bias vectors) will be hidden for a cleaner\n        visualization.\n\n    Returns\n    -------\n    dot: Digraph\n        A Graphviz digraph object visualizing the computation graph to compute `symbol`.\n\n    Example\n    -------\n    >>> net = mx.sym.Variable(\'data\')\n    >>> net = mx.sym.FullyConnected(data=net, name=\'fc1\', num_hidden=128)\n    >>> net = mx.sym.Activation(data=net, name=\'relu1\', act_type="relu")\n    >>> net = mx.sym.FullyConnected(data=net, name=\'fc2\', num_hidden=10)\n    >>> net = mx.sym.SoftmaxOutput(data=net, name=\'out\')\n    >>> digraph = mx.viz.plot_network(net, shape={\'data\':(100,200)},\n    ... node_attrs={"fixedsize":"false"})\n    >>> digraph.view()\n    '
    try:
        from graphviz import Digraph
    except:
        raise ImportError('Draw network requires graphviz library')
    if (not isinstance(symbol, Symbol)):
        raise TypeError('symbol must be a Symbol')
    draw_shape = False
    if (shape is not None):
        draw_shape = True
        interals = symbol.get_internals()
        (_, out_shapes, _) = interals.infer_shape(**shape)
        if (out_shapes is None):
            raise ValueError('Input shape is incomplete')
        shape_dict = dict(zip(interals.list_outputs(), out_shapes))
    conf = json.loads(symbol.tojson())
    nodes = conf['nodes']
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
        if name.endswith('_weight'):
            return True
        if name.endswith('_bias'):
            return True
        if (name.endswith('_beta') or name.endswith('_gamma') or name.endswith('_moving_var') or name.endswith('_moving_mean')):
            return True
        return False
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
            label = ('Convolution\\n%s/%s, %s' % ('x'.join(_str2tuple(node['attrs']['kernel'])), ('x'.join(_str2tuple(node['attrs']['stride'])) if ('stride' in node['attrs']) else '1'), node['attrs']['num_filter']))
            attr['fillcolor'] = cm[1]
        elif (op == 'FullyConnected'):
            label = ('FullyConnected\\n%s' % node['attrs']['num_hidden'])
            attr['fillcolor'] = cm[1]
        elif (op == 'BatchNorm'):
            attr['fillcolor'] = cm[3]
        elif ((op == 'Activation') or (op == 'LeakyReLU')):
            label = ('%s\\n%s' % (op, node['attrs']['act_type']))
            attr['fillcolor'] = cm[2]
        elif (op == 'Pooling'):
            label = ('Pooling\\n%s, %s/%s' % (node['attrs']['pool_type'], 'x'.join(_str2tuple(node['attrs']['kernel'])), ('x'.join(_str2tuple(node['attrs']['stride'])) if ('stride' in node['attrs']) else '1')))
            attr['fillcolor'] = cm[4]
        elif ((op == 'Concat') or (op == 'Flatten') or (op == 'Reshape')):
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
                    dot.edge(tail_name=name, head_name=input_name, **attr)
    return dot
