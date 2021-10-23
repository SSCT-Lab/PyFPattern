def _parse_proto(prototxt_fname):
    'Parse Caffe prototxt into symbol string\n    '
    proto = caffe_parser.read_prototxt(prototxt_fname)
    (input_name, input_dim, layers) = _get_input(proto)
    mapping = {
        input_name: 'data',
    }
    need_flatten = {
        input_name: False,
    }
    symbol_string = "import mxnet as mx\ndata = mx.symbol.Variable(name='data')\n"
    flatten_count = 0
    output_name = ''
    prev_name = None
    _output_name = {
        
    }
    for (i, layer) in enumerate(layers):
        type_string = ''
        param_string = ''
        skip_layer = False
        name = re.sub('[-/]', '_', layer.name)
        for k in range(len(layer.bottom)):
            if (layer.bottom[k] in _output_name):
                _output_name[layer.bottom[k]]['count'] = (_output_name[layer.bottom[k]]['count'] + 1)
            else:
                _output_name[layer.bottom[k]] = {
                    'count': 0,
                }
        for k in range(len(layer.top)):
            if (layer.top[k] in _output_name):
                _output_name[layer.top[k]]['count'] = (_output_name[layer.top[k]]['count'] + 1)
            else:
                _output_name[layer.top[k]] = {
                    'count': 0,
                    'name': name,
                }
        if ((layer.type == 'Convolution') or (layer.type == 4)):
            type_string = 'mx.symbol.Convolution'
            param_string = _convert_conv_param(layer.convolution_param)
            need_flatten[name] = True
        if ((layer.type == 'Deconvolution') or (layer.type == 39)):
            type_string = 'mx.symbol.Deconvolution'
            param_string = _convert_conv_param(layer.convolution_param)
            need_flatten[name] = True
        if ((layer.type == 'Pooling') or (layer.type == 17)):
            type_string = 'mx.symbol.Pooling'
            param_string = _convert_pooling_param(layer.pooling_param)
            need_flatten[name] = True
        if ((layer.type == 'ReLU') or (layer.type == 18)):
            type_string = 'mx.symbol.Activation'
            param_string = "act_type='relu'"
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if ((layer.type == 'TanH') or (layer.type == 23)):
            type_string = 'mx.symbol.Activation'
            param_string = "act_type='tanh'"
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if ((layer.type == 'Sigmoid') or (layer.type == 19)):
            type_string = 'mx.symbol.Activation'
            param_string = "act_type='sigmoid'"
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if ((layer.type == 'LRN') or (layer.type == 15)):
            type_string = 'mx.symbol.LRN'
            param = layer.lrn_param
            param_string = ('alpha=%f, beta=%f, knorm=%f, nsize=%d' % (param.alpha, param.beta, param.k, param.local_size))
            need_flatten[name] = True
        if ((layer.type == 'InnerProduct') or (layer.type == 14)):
            type_string = 'mx.symbol.FullyConnected'
            param = layer.inner_product_param
            param_string = ('num_hidden=%d, no_bias=%s' % (param.num_output, (not param.bias_term)))
            need_flatten[name] = False
        if ((layer.type == 'Dropout') or (layer.type == 6)):
            type_string = 'mx.symbol.Dropout'
            param = layer.dropout_param
            param_string = ('p=%f' % param.dropout_ratio)
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if ((layer.type == 'Softmax') or (layer.type == 20)):
            type_string = 'mx.symbol.SoftmaxOutput'
        if ((layer.type == 'Flatten') or (layer.type == 8)):
            type_string = 'mx.symbol.Flatten'
            need_flatten[name] = False
        if ((layer.type == 'Split') or (layer.type == 22)):
            type_string = 'split'
        if ((layer.type == 'Concat') or (layer.type == 3)):
            type_string = 'mx.symbol.Concat'
            need_flatten[name] = True
        if (layer.type == 'Crop'):
            type_string = 'mx.symbol.Crop'
            need_flatten[name] = True
            param_string = 'center_crop=True'
        if (layer.type == 'BatchNorm'):
            type_string = 'mx.symbol.BatchNorm'
            param = layer.batch_norm_param
            epsilon = param.eps
            if (epsilon <= 1e-05):
                epsilon = 0.0001
            fix_gamma = (layers[(i + 1)].type != 'Scale')
            param_string = ('use_global_stats=%s, fix_gamma=%s, eps=%f' % (param.use_global_stats, fix_gamma, epsilon))
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if (layer.type == 'Scale'):
            assert (layers[(i - 1)].type == 'BatchNorm')
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
            skip_layer = True
            prev_name = re.sub('[-/]', '_', layers[(i - 1)].name)
        if (layer.type == 'PReLU'):
            type_string = 'mx.symbol.LeakyReLU'
            param = layer.prelu_param
            param_string = ("act_type='prelu', slope=%f" % param.filler.value)
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if (layer.type == 'Eltwise'):
            type_string = 'mx.symbol.broadcast_add'
            param = layer.eltwise_param
            param_string = ''
            need_flatten[name] = False
        if (layer.type == 'Reshape'):
            type_string = 'mx.symbol.Reshape'
            need_flatten[name] = False
            param = layer.reshape_param
            param_string = ('shape=(%s)' % (','.join(param.shape.dim),))
        if (layer.type == 'AbsVal'):
            type_string = 'mx.symbol.abs'
            need_flatten[name] = need_flatten[mapping[layer.bottom[0]]]
        if skip_layer:
            assert (len(layer.bottom) == 1)
            symbol_string += ('%s = %s\n' % (name, prev_name))
        elif (type_string == ''):
            raise ValueError(('Unknown layer %s!' % layer.type))
        elif (type_string != 'split'):
            bottom = layer.bottom
            if (param_string != ''):
                param_string = (', ' + param_string)
            if (len(bottom) == 1):
                if (need_flatten[mapping[bottom[0]]] and (type_string == 'mx.symbol.FullyConnected')):
                    flatten_name = ('flatten_%d' % flatten_count)
                    symbol_string += ("%s=mx.symbol.Flatten(name='%s', data=%s)\n" % (flatten_name, flatten_name, mapping[bottom[0]]))
                    flatten_count += 1
                    need_flatten[flatten_name] = False
                    bottom[0] = flatten_name
                    mapping[bottom[0]] = bottom[0]
                symbol_string += ("%s = %s(name='%s', data=%s %s)\n" % (name, type_string, name, mapping[bottom[0]], param_string))
            elif ((layer.type == 'Eltwise') and (param.operation == 1) and (len(param.coeff) > 0)):
                symbol_string += ('%s = ' % name)
                symbol_string += ' + '.join([('%s * %s' % (mapping[bottom[i]], param.coeff[i])) for i in range(len(param.coeff))])
                symbol_string += '\n'
            else:
                symbol_string += ("%s = %s(name='%s', *[%s] %s)\n" % (name, type_string, name, ','.join([mapping[x] for x in bottom]), param_string))
        for j in range(len(layer.top)):
            mapping[layer.top[j]] = name
        output_name = name
    output_name = []
    for i in _output_name:
        if (('name' in _output_name[i]) and (_output_name[i]['count'] == 0)):
            output_name.append(_output_name[i]['name'])
    return (symbol_string, output_name, input_dim)