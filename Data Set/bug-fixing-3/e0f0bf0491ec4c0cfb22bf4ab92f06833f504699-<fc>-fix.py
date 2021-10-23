def fc(net, num_hidden, act_type, weight=None, bias=None, no_bias=False):
    if ((weight is None) and (bias is None)):
        net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, no_bias=no_bias)
    elif ((weight is None) and (bias is not None)):
        if no_bias:
            net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, no_bias=no_bias)
        else:
            net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, bias=bias, no_bias=no_bias)
    elif ((weight is not None) and (bias is None)):
        net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, weight=weight, no_bias=no_bias)
    elif no_bias:
        net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, weight=weight, no_bias=no_bias)
    else:
        net = mx.sym.FullyConnected(data=net, num_hidden=num_hidden, weight=weight, bias=bias, no_bias=no_bias)
    if (act_type is not None):
        net = mx.sym.Activation(data=net, act_type=act_type)
    return net