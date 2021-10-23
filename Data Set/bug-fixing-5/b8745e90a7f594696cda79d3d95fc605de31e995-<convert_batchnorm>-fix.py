def convert_batchnorm(net, node, module, builder):
    'Convert a batchnorm layer from mxnet to coreml.\n\n    Parameters\n    ----------\n    network: net\n        A mxnet network object.\n\n    layer: node\n        Node to convert.\n\n    module: module\n        An module for MXNet\n\n    builder: NeuralNetworkBuilder\n        A neural network builder object.\n    '
    (input_name, output_name) = _get_input_output_name(net, node)
    name = node['name']
    inputs = node['inputs']
    eps = 0.001
    use_global_stats = False
    if ('attr' in node):
        if ('eps' in node['attr']):
            eps = literal_eval(node['attr']['eps'])
    (args, aux) = module.get_params()
    gamma = args[_get_node_name(net, inputs[1][0])].asnumpy()
    beta = args[_get_node_name(net, inputs[2][0])].asnumpy()
    mean = aux[_get_node_name(net, inputs[3][0])].asnumpy()
    variance = aux[_get_node_name(net, inputs[4][0])].asnumpy()
    nb_channels = gamma.shape[0]
    builder.add_batchnorm(name=name, channels=nb_channels, gamma=gamma, beta=beta, mean=mean, variance=variance, input_name=input_name, output_name=output_name, epsilon=eps)