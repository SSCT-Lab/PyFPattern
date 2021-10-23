def resnet50_v2a(pretrained=False, root='~/.mxnet/models', ctx=mx.cpu(0), **kwargs):
    "Constructs a ResNet50-v2a model.\n\n    Please ignore this if you are looking for model for other tasks.\n\n    Parameters\n    ----------\n    pretrained : bool, default False\n        Whether to load the pretrained weights for model.\n    root : str, default '~/.mxnet/models'\n        Location for keeping the model parameters.\n    ctx : Context, default mx.cpu(0)\n        The context in which to load the pretrained weights.\n    norm_layer : object\n        Normalization layer used in backbone network (default: :class:`mxnet.gluon.nn.BatchNorm`;\n    "
    model = ResNet50V2(prefix='', **kwargs)
    if pretrained:
        from ..model_store import get_model_file
        model.load_params(get_model_file(('resnet%d_v%da' % (50, 2)), root=root), ctx=ctx, allow_missing=True)
        for v in model.collect_params(select='init_scale|init_mean').values():
            v.initialize(force_reinit=True)
    return model