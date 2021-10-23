def get_resnet(version, num_layers, pretrained=False, ctx=cpu(), root='~/.mxnet/models', use_se=False, **kwargs):
    'ResNet V1 model from `"Deep Residual Learning for Image Recognition"\n    <http://arxiv.org/abs/1512.03385>`_ paper.\n    ResNet V2 model from `"Identity Mappings in Deep Residual Networks"\n    <https://arxiv.org/abs/1603.05027>`_ paper.\n\n    Parameters\n    ----------\n    version : int\n        Version of ResNet. Options are 1, 2.\n    num_layers : int\n        Numbers of layers. Options are 18, 34, 50, 101, 152.\n    pretrained : bool or str\n        Boolean value controls whether to load the default pretrained weights for model.\n        String value represents the hashtag for a certain version of pretrained weights.\n    ctx : Context, default CPU\n        The context in which to load the pretrained weights.\n    root : str, default $MXNET_HOME/models\n        Location for keeping the model parameters.\n    use_se : bool, default False\n        Whether to use Squeeze-and-Excitation module\n    norm_layer : object\n        Normalization layer used (default: :class:`mxnet.gluon.nn.BatchNorm`)\n        Can be :class:`mxnet.gluon.nn.BatchNorm` or :class:`mxnet.gluon.contrib.nn.SyncBatchNorm`.\n    norm_kwargs : dict\n        Additional `norm_layer` arguments, for example `num_devices=4`\n        for :class:`mxnet.gluon.contrib.nn.SyncBatchNorm`.\n    '
    assert (num_layers in resnet_spec), ('Invalid number of layers: %d. Options are %s' % (num_layers, str(resnet_spec.keys())))
    (block_type, layers, channels) = resnet_spec[num_layers]
    assert (1 <= version <= 2), ('Invalid resnet version: %d. Options are 1 and 2.' % version)
    resnet_class = resnet_net_versions[(version - 1)]
    block_class = resnet_block_versions[(version - 1)][block_type]
    net = resnet_class(block_class, layers, channels, use_se=use_se, **kwargs)
    if pretrained:
        from .model_store import get_model_file
        if (not use_se):
            net.load_parameters(get_model_file(('resnet%d_v%d' % (num_layers, version)), tag=pretrained, root=root), ctx=ctx)
        else:
            net.load_parameters(get_model_file(('se_resnet%d_v%d' % (num_layers, version)), tag=pretrained, root=root), ctx=ctx)
        from ..data import ImageNet1kAttr
        attrib = ImageNet1kAttr()
        net.synset = attrib.synset
        net.classes = attrib.classes
        net.classes_long = attrib.classes_long
    return net