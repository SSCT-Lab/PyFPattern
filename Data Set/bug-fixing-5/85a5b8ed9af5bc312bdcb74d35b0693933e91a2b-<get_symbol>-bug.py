def get_symbol(network, batch_size):
    image_shape = ((3, 299, 299) if (network == 'inception-v3') else (3, 224, 224))
    num_layers = 0
    if ('resnet' in network):
        num_layers = int(network.split('-')[1])
        network = 'resnet'
    net = import_module(('symbols.' + network))
    sym = net.get_symbol(num_classes=1000, image_shape=','.join([str(i) for i in image_shape]), num_layers=num_layers)
    return (sym, [('data', ((batch_size,) + image_shape))])