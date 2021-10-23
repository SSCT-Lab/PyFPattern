def evaluate_net(net, path_imgrec, num_classes, mean_pixels, data_shape, model_prefix, epoch, ctx=mx.cpu(), batch_size=1, path_imglist='', nms_thresh=0.45, force_nms=False, ovp_thresh=0.5, use_difficult=False, class_names=None, voc07_metric=False):
    '\n    evalute network given validation record file\n\n    Parameters:\n    ----------\n    net : str or None\n        Network name or use None to load from json without modifying\n    path_imgrec : str\n        path to the record validation file\n    path_imglist : str\n        path to the list file to replace labels in record file, optional\n    num_classes : int\n        number of classes, not including background\n    mean_pixels : tuple\n        (mean_r, mean_g, mean_b)\n    data_shape : tuple or int\n        (3, height, width) or height/width\n    model_prefix : str\n        model prefix of saved checkpoint\n    epoch : int\n        load model epoch\n    ctx : mx.ctx\n        mx.gpu() or mx.cpu()\n    batch_size : int\n        validation batch size\n    nms_thresh : float\n        non-maximum suppression threshold\n    force_nms : boolean\n        whether suppress different class objects\n    ovp_thresh : float\n        AP overlap threshold for true/false postives\n    use_difficult : boolean\n        whether to use difficult objects in evaluation if applicable\n    class_names : comma separated str\n        class names in string, must correspond to num_classes if set\n    voc07_metric : boolean\n        whether to use 11-point evluation as in VOC07 competition\n    '
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if isinstance(data_shape, int):
        data_shape = (3, data_shape, data_shape)
    assert ((len(data_shape) == 3) and (data_shape[0] == 3))
    model_prefix += ('_' + str(data_shape[1]))
    eval_iter = DetRecordIter(path_imgrec, batch_size, data_shape, mean_pixels=mean_pixels, path_imglist=path_imglist, **cfg.valid)
    (load_net, args, auxs) = mx.model.load_checkpoint(model_prefix, epoch)
    if (net is None):
        net = load_net
    else:
        net = get_symbol(net, data_shape[1], num_classes=num_classes, nms_thresh=nms_thresh, force_suppress=force_nms)
    if (not ('label' in net.list_arguments())):
        label = mx.sym.Variable(name='label')
        net = mx.sym.Group([net, label])
    mod = mx.mod.Module(net, label_names=('label',), logger=logger, context=ctx, fixed_param_names=net.list_arguments())
    mod.bind(data_shapes=eval_iter.provide_data, label_shapes=eval_iter.provide_label)
    mod.set_params(args, auxs, allow_missing=False, force_init=True)
    if voc07_metric:
        metric = VOC07MApMetric(ovp_thresh, use_difficult, class_names)
    else:
        metric = MApMetric(ovp_thresh, use_difficult, class_names)
    results = mod.score(eval_iter, metric, num_batch=None)
    for (k, v) in results:
        print('{}: {}'.format(k, v))