def print_summary(symbol, shape=None, line_length=120, positions=[0.44, 0.64, 0.74, 1.0]):
    'Convert symbol for detail information.\n\n    Parameters\n    ----------\n    symbol: Symbol\n        Symbol to be visualized.\n    shape: dict\n        A dict of shapes, str->shape (tuple), given input shapes.\n    line_length: int\n        Rotal length of printed lines\n    positions: list\n        Relative or absolute positions of log elements in each line.\n    Returns\n    ------\n    None\n    '
    if (not isinstance(symbol, Symbol)):
        raise TypeError('symbol must be Symbol')
    show_shape = False
    if (shape is not None):
        show_shape = True
        interals = symbol.get_internals()
        (_, out_shapes, _) = interals.infer_shape(**shape)
        if (out_shapes is None):
            raise ValueError('Input shape is incomplete')
        shape_dict = dict(zip(interals.list_outputs(), out_shapes))
    conf = json.loads(symbol.tojson())
    nodes = conf['nodes']
    heads = set(conf['heads'][0])
    if (positions[(- 1)] <= 1):
        positions = [int((line_length * p)) for p in positions]
    to_display = ['Layer (type)', 'Output Shape', 'Param #', 'Previous Layer']

    def print_row(fields, positions):
        'Print format row.\n\n        Parameters\n        ----------\n        fields: list\n            Information field.\n        positions: list\n            Field length ratio.\n        Returns\n        ------\n        None\n        '
        line = ''
        for (i, field) in enumerate(fields):
            line += str(field)
            line = line[:positions[i]]
            line += (' ' * (positions[i] - len(line)))
        print(line)
    print(('_' * line_length))
    print_row(to_display, positions)
    print(('=' * line_length))

    def print_layer_summary(node, out_shape):
        'print layer information\n\n        Parameters\n        ----------\n        node: dict\n            Node information.\n        out_shape: dict\n            Node shape information.\n        Returns\n        ------\n            Node total parameters.\n        '
        op = node['op']
        pre_node = []
        pre_filter = 0
        if (op != 'null'):
            inputs = node['inputs']
            for item in inputs:
                input_node = nodes[item[0]]
                input_name = input_node['name']
                if ((input_node['op'] != 'null') or (item[0] in heads)):
                    pre_node.append(input_name)
                    if show_shape:
                        if (input_node['op'] != 'null'):
                            key = (input_name + '_output')
                        else:
                            key = input_name
                        if (key in shape_dict):
                            shape = shape_dict[key][1:]
                            pre_filter = (pre_filter + int(shape[0]))
        cur_param = 0
        if (op == 'Convolution'):
            if (('no_bias' in node['attrs']) and (node['attrs']['no_bias'] == 'True')):
                num_group = int(node['attrs'].get('num_group', '1'))
                cur_param = ((pre_filter * int(node['attrs']['num_filter'])) // num_group)
                for k in _str2tuple(node['attrs']['kernel']):
                    cur_param *= int(k)
            else:
                num_group = int(node['attrs'].get('num_group', '1'))
                cur_param = ((pre_filter * int(node['attrs']['num_filter'])) // num_group)
                for k in _str2tuple(node['attrs']['kernel']):
                    cur_param *= int(k)
                cur_param += int(node['attrs']['num_filter'])
        elif (op == 'FullyConnected'):
            if (('no_bias' in node['attrs']) and (node['attrs']['no_bias'] == 'True')):
                cur_param = (pre_filter * int(node['attrs']['num_hidden']))
            else:
                cur_param = ((pre_filter + 1) * int(node['attrs']['num_hidden']))
        elif (op == 'BatchNorm'):
            key = (node['name'] + '_output')
            if show_shape:
                num_filter = shape_dict[key][1]
                cur_param = (int(num_filter) * 2)
        if (not pre_node):
            first_connection = ''
        else:
            first_connection = pre_node[0]
        fields = [(((node['name'] + '(') + op) + ')'), 'x'.join([str(x) for x in out_shape]), cur_param, first_connection]
        print_row(fields, positions)
        if (len(pre_node) > 1):
            for i in range(1, len(pre_node)):
                fields = ['', '', '', pre_node[i]]
                print_row(fields, positions)
        return cur_param
    total_params = 0
    for (i, node) in enumerate(nodes):
        out_shape = []
        op = node['op']
        if ((op == 'null') and (i > 0)):
            continue
        if ((op != 'null') or (i in heads)):
            if show_shape:
                if (op != 'null'):
                    key = (node['name'] + '_output')
                else:
                    key = node['name']
                if (key in shape_dict):
                    out_shape = shape_dict[key][1:]
        total_params += print_layer_summary(nodes[i], out_shape)
        if (i == (len(nodes) - 1)):
            print(('=' * line_length))
        else:
            print(('_' * line_length))
    print(('Total params: %s' % total_params))
    print(('_' * line_length))