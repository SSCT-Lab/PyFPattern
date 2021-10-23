def get_fine_tune_model(symbol, arg_params, num_classes, layer_name):
    '\n    symbol: the pre-trained network symbol\n    arg_params: the argument parameters of the pre-trained model\n    num_classes: the number of classes for the fine-tune datasets\n    layer_name: the layer name before the last fully-connected layer\n    '
    all_layers = sym.get_internals()
    net = all_layers[(layer_name + '_output')]
    net = mx.symbol.FullyConnected(data=net, num_hidden=num_classes, name='fc')
    net = mx.symbol.SoftmaxOutput(data=net, name='softmax')
    new_args = dict({k: arg_params[k] for k in arg_params if ('fc' not in k)})
    return (net, new_args)