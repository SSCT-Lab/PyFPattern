def sequence_fc(net, seq_len, num_layer, prefix, num_hidden_list=[], act_type_list=[], is_batchnorm=False, dropout_rate=0):
    if (num_layer == len(num_hidden_list) == len(act_type_list)):
        if (num_layer > 0):
            weight_list = []
            bias_list = []
            for layer_index in range(num_layer):
                weight_list.append(mx.sym.Variable(name=('%s_sequence_fc%d_weight' % (prefix, layer_index))))
                if (not is_batchnorm):
                    bias_list.append(mx.sym.Variable(name=('%s_sequence_fc%d_bias' % (prefix, layer_index))))
            gamma_list = []
            beta_list = []
            if is_batchnorm:
                for layer_index in range(num_layer):
                    gamma_list.append(mx.sym.Variable(name=('%s_sequence_fc%d_gamma' % (prefix, layer_index))))
                    beta_list.append(mx.sym.Variable(name=('%s_sequence_fc%d_beta' % (prefix, layer_index))))
            if (type(net) is mx.symbol.Symbol):
                net = mx.sym.SliceChannel(data=net, num_outputs=seq_len, axis=1, squeeze_axis=1)
            elif (type(net) is list):
                for (net_index, one_net) in enumerate(net):
                    if (type(one_net) is not mx.symbol.Symbol):
                        raise Exception(('%d th elements of the net should be mx.symbol.Symbol' % net_index))
            else:
                raise Exception('type of net should be whether mx.symbol.Symbol or list of mx.symbol.Symbol')
            hidden_all = []
            for seq_index in range(seq_len):
                hidden = net[seq_index]
                for layer_index in range(num_layer):
                    if (dropout_rate > 0):
                        hidden = mx.sym.Dropout(data=hidden, p=dropout_rate)
                    if is_batchnorm:
                        hidden = fc(net=hidden, num_hidden=num_hidden_list[layer_index], act_type=None, weight=weight_list[layer_index], no_bias=is_batchnorm)
                        hidden = batchnorm(net=hidden, gamma=gamma_list[layer_index], beta=beta_list[layer_index])
                        hidden = mx.sym.Activation(data=hidden, act_type=act_type_list[layer_index])
                    else:
                        hidden = fc(net=hidden, num_hidden=num_hidden_list[layer_index], act_type=act_type_list[layer_index], weight=weight_list[layer_index], bias=bias_list[layer_index])
                hidden_all.append(hidden)
            net = hidden_all
        return net
    else:
        raise Exception("length doesn't met - num_layer:", num_layer, ',len(num_hidden_list):', len(num_hidden_list), ',len(act_type_list):', len(act_type_list))