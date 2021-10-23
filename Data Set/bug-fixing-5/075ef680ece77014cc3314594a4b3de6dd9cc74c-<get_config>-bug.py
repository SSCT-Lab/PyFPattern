def get_config(network, data_shape, **kwargs):
    'Configuration factory for various networks\n\n    Parameters\n    ----------\n    network : str\n        base network name, such as vgg_reduced, inceptionv3, resnet...\n    data_shape : int\n        input data dimension\n    kwargs : dict\n        extra arguments\n    '
    if (network == 'vgg16_reduced'):
        if (data_shape >= 448):
            from_layers = ['relu4_3', 'relu7', '', '', '', '', '']
            num_filters = [512, (- 1), 512, 256, 256, 256, 256]
            strides = [(- 1), (- 1), 2, 2, 2, 2, 1]
            pads = [(- 1), (- 1), 1, 1, 1, 1, 1]
            sizes = [[0.07, 0.1025], [0.15, 0.2121], [0.3, 0.3674], [0.45, 0.5196], [0.6, 0.6708], [0.75, 0.8216], [0.9, 0.9721]]
            ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5], [1, 2, 0.5]]
            normalizations = [20, (- 1), (- 1), (- 1), (- 1), (- 1), (- 1)]
            steps = ([] if (data_shape != 512) else [(x / 512.0) for x in [8, 16, 32, 64, 128, 256, 512]])
        else:
            from_layers = ['relu4_3', 'relu7', '', '', '', '']
            num_filters = [512, (- 1), 512, 256, 256, 256]
            strides = [(- 1), (- 1), 2, 2, 1, 1]
            pads = [(- 1), (- 1), 1, 1, 0, 0]
            sizes = [[0.1, 0.141], [0.2, 0.272], [0.37, 0.447], [0.54, 0.619], [0.71, 0.79], [0.88, 0.961]]
            ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5], [1, 2, 0.5]]
            normalizations = [20, (- 1), (- 1), (- 1), (- 1), (- 1)]
            steps = ([] if (data_shape != 300) else [(x / 300.0) for x in [8, 16, 32, 64, 100, 300]])
        if (not ((data_shape == 300) or (data_shape == 512))):
            logging.warn(('data_shape %d was not tested, use with caucious.' % data_shape))
        return locals()
    elif (network == 'inceptionv3'):
        from_layers = ['ch_concat_mixed_7_chconcat', 'ch_concat_mixed_10_chconcat', '', '', '', '']
        num_filters = [(- 1), (- 1), 512, 256, 256, 128]
        strides = [(- 1), (- 1), 2, 2, 2, 2]
        pads = [(- 1), (- 1), 1, 1, 1, 1]
        sizes = [[0.1, 0.141], [0.2, 0.272], [0.37, 0.447], [0.54, 0.619], [0.71, 0.79], [0.88, 0.961]]
        ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5], [1, 2, 0.5]]
        normalizations = (- 1)
        steps = []
        return locals()
    elif (network == 'resnet50'):
        num_layers = 50
        image_shape = '3,224,224'
        network = 'resnet'
        from_layers = ['_plus12', '_plus15', '', '', '', '']
        num_filters = [(- 1), (- 1), 512, 256, 256, 128]
        strides = [(- 1), (- 1), 2, 2, 2, 2]
        pads = [(- 1), (- 1), 1, 1, 1, 1]
        sizes = [[0.1, 0.141], [0.2, 0.272], [0.37, 0.447], [0.54, 0.619], [0.71, 0.79], [0.88, 0.961]]
        ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5], [1, 2, 0.5]]
        normalizations = (- 1)
        steps = []
        return locals()
    elif (network == 'resnet101'):
        num_layers = 101
        image_shape = '3,224,224'
        network = 'resnet'
        from_layers = ['_plus12', '_plus15', '', '', '', '']
        num_filters = [(- 1), (- 1), 512, 256, 256, 128]
        strides = [(- 1), (- 1), 2, 2, 2, 2]
        pads = [(- 1), (- 1), 1, 1, 1, 1]
        sizes = [[0.1, 0.141], [0.2, 0.272], [0.37, 0.447], [0.54, 0.619], [0.71, 0.79], [0.88, 0.961]]
        ratios = [[1, 2, 0.5], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5, 3, (1.0 / 3)], [1, 2, 0.5], [1, 2, 0.5]]
        normalizations = (- 1)
        steps = []
        return locals()
    else:
        msg = ('No configuration found for %s with data_shape %d' % (network, data_shape))
        raise NotImplementedError(msg)