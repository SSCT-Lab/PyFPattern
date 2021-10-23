

def plot_network(symbol, title='plot', shape=None, node_attrs={
    
}):
    'convert symbol to dot object for visualization\n\n    Parameters\n    ----------\n    title: str\n        title of the dot graph\n    symbol: Symbol\n        symbol to be visualized\n    shape: dict\n        dict of shapes, str->shape (tuple), given input shapes\n    node_attrs: dict\n        dict of node\'s attributes\n        for example:\n            node_attrs={"shape":"oval","fixedsize":"fasle"}\n            means to plot the network in "oval"\n    Returns\n    ------\n    dot: Diagraph\n        dot object of symbol\n    '
    try:
        from graphviz import Digraph
    except:
        raise ImportError('Draw network requires graphviz library')
    if (not isinstance(symbol, Symbol)):
        raise TypeError('symbol must be Symbol')
    draw_shape = False
    if (shape != None):
        draw_shape = True
        interals = symbol.get_internals()
        (_, out_shapes, _) = interals.infer_shape(**shape)
        if (out_shapes == None):
            raise ValueError('Input shape is incompete')
        shape_dict = dict(zip(interals.list_outputs(), out_shapes))
    conf = json.loads(symbol.tojson())
    nodes = conf['nodes']
    heads = set(conf['heads'][0])
    node_attr = {
        'shape': 'box',
        'fixedsize': 'true',
        'width': '1.3',
        'height': '0.8034',
        'style': 'filled',
    }
    node_attr.update(node_attrs)
    dot = Digraph(name=title)
    cm = ('#8dd3c7', '#fb8072', '#ffffb3', '#bebada', '#80b1d3', '#fdb462', '#b3de69', '#fccde5')
    for i in range(len(nodes)):
        node = nodes[i]
        op = node['op']
        name = node['name']
        attr = copy.deepcopy(node_attr)
        label = op
        if (op == 'null'):
            if (i in heads):
                label = node['name']
                attr['fillcolor'] = cm[0]
            else:
                continue
        elif (op == 'Convolution'):
            label = ('Convolution\\n%sx%s/%s, %s' % (_str2tuple(node['param']['kernel'])[0], _str2tuple(node['param']['kernel'])[1], _str2tuple(node['param']['stride'])[0], node['param']['num_filter']))
            attr['fillcolor'] = cm[1]
        elif (op == 'FullyConnected'):
            label = ('FullyConnected\\n%s' % node['param']['num_hidden'])
            attr['fillcolor'] = cm[1]
        elif (op == 'BatchNorm'):
            attr['fillcolor'] = cm[3]
        elif ((op == 'Activation') or (op == 'LeakyReLU')):
            label = ('%s\\n%s' % (op, node['param']['act_type']))
            attr['fillcolor'] = cm[2]
        elif (op == 'Pooling'):
            label = ('Pooling\\n%s, %sx%s/%s' % (node['param']['pool_type'], _str2tuple(node['param']['kernel'])[0], _str2tuple(node['param']['kernel'])[1], _str2tuple(node['param']['stride'])[0]))
            attr['fillcolor'] = cm[4]
        elif ((op == 'Concat') or (op == 'Flatten') or (op == 'Reshape')):
            attr['fillcolor'] = cm[5]
        elif (op == 'Softmax'):
            attr['fillcolor'] = cm[6]
        else:
            attr['fillcolor'] = cm[7]
        dot.node(name=name, label=label, **attr)
    for i in range(len(nodes)):
        node = nodes[i]
        op = node['op']
        name = node['name']
        if (op == 'null'):
            continue
        else:
            inputs = node['inputs']
            for item in inputs:
                input_node = nodes[item[0]]
                input_name = input_node['name']
                if ((input_node['op'] != 'null') or (item[0] in heads)):
                    attr = {
                        'dir': 'back',
                        'arrowtail': 'open',
                    }
                    if draw_shape:
                        if (input_node['op'] != 'null'):
                            key = (input_name + '_output')
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
