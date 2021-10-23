def ssd_512_resnet18_v1_custom(classes, pretrained_base=True, transfer=None, **kwargs):
    "SSD architecture with ResNet18 v1 512 base network for COCO.\n\n    Parameters\n    ----------\n    classes : iterable of str\n        Names of custom foreground classes. `len(classes)` is the number of foreground classes.\n    pretrained_base : bool or str, optional, default is True\n        Load pretrained base network, the extra layers are randomized.\n    transfer : str or None\n        If not `None`, will try to reuse pre-trained weights from SSD networks trained on other\n        datasets.\n\n    Returns\n    -------\n    HybridBlock\n        A SSD detection network.\n\n    Example\n    -------\n    >>> net = ssd_512_resnet18_v1_custom(classes=['a', 'b', 'c'], pretrained_base=True)\n    >>> net = ssd_512_resnet18_v1_custom(classes=['foo', 'bar'], transfer='voc')\n\n    "
    if (transfer is None):
        kwargs['pretrained'] = False
        net = get_ssd('resnet18_v1', 512, features=['stage3_activation1', 'stage4_activation1'], filters=[512, 512, 256, 256], sizes=[51.2, 102.4, 189.4, 276.4, 363.52, 450.6, 492], ratios=(([[1, 2, 0.5]] + ([[1, 2, 0.5, 3, (1.0 / 3)]] * 3)) + ([[1, 2, 0.5]] * 2)), steps=[16, 32, 64, 128, 256, 512], classes=classes, dataset='', pretrained_base=pretrained_base, **kwargs)
    else:
        from ...model_zoo import get_model
        net = get_model(('ssd_512_resnet18_v1_' + str(transfer)), pretrained=True, **kwargs)
        net.reset_class(classes)
    return net