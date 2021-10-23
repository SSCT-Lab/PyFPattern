def __init__(self, network, base_size, features, num_filters, sizes, ratios, steps, classes, use_1x1_transition=True, use_bn=True, reduce_ratio=1.0, min_depth=128, global_pool=False, pretrained=False, stds=(0.1, 0.1, 0.2, 0.2), nms_thresh=0.45, nms_topk=400, post_nms=100, anchor_alloc_size=128, ctx=mx.cpu(), norm_layer=nn.BatchNorm, norm_kwargs=None, root=os.path.join('~', '.mxnet', 'models'), **kwargs):
    super(SSD, self).__init__(**kwargs)
    if (norm_kwargs is None):
        norm_kwargs = {
            
        }
    if (network is None):
        num_layers = len(ratios)
    else:
        num_layers = ((len(features) + len(num_filters)) + int(global_pool))
    assert (len(sizes) == (num_layers + 1))
    sizes = list(zip(sizes[:(- 1)], sizes[1:]))
    assert isinstance(ratios, list), 'Must provide ratios as list or list of list'
    if (not isinstance(ratios[0], (tuple, list))):
        ratios = (ratios * num_layers)
    assert (num_layers == len(sizes) == len(ratios)), 'Mismatched (number of layers) vs (sizes) vs (ratios): {}, {}, {}'.format(num_layers, len(sizes), len(ratios))
    assert (num_layers > 0), 'SSD require at least one layer, suggest multiple.'
    self._num_layers = num_layers
    self.classes = classes
    self.nms_thresh = nms_thresh
    self.nms_topk = nms_topk
    self.post_nms = post_nms
    with self.name_scope():
        if (network is None):
            try:
                self.features = features(pretrained=pretrained, ctx=ctx, root=root, norm_layer=norm_layer, norm_kwargs=norm_kwargs)
            except TypeError:
                self.features = features(pretrained=pretrained, ctx=ctx, root=root)
        else:
            try:
                self.features = FeatureExpander(network=network, outputs=features, num_filters=num_filters, use_1x1_transition=use_1x1_transition, use_bn=use_bn, reduce_ratio=reduce_ratio, min_depth=min_depth, global_pool=global_pool, pretrained=pretrained, ctx=ctx, norm_layer=norm_layer, norm_kwargs=norm_kwargs, root=root)
            except TypeError:
                self.features = FeatureExpander(network=network, outputs=features, num_filters=num_filters, use_1x1_transition=use_1x1_transition, use_bn=use_bn, reduce_ratio=reduce_ratio, min_depth=min_depth, global_pool=global_pool, pretrained=pretrained, ctx=ctx, root=root)
        self.class_predictors = nn.HybridSequential()
        self.box_predictors = nn.HybridSequential()
        self.anchor_generators = nn.HybridSequential()
        asz = anchor_alloc_size
        im_size = (base_size, base_size)
        for (i, s, r, st) in zip(range(num_layers), sizes, ratios, steps):
            anchor_generator = SSDAnchorGenerator(i, im_size, s, r, st, (asz, asz))
            self.anchor_generators.add(anchor_generator)
            asz = max((asz // 2), 16)
            num_anchors = anchor_generator.num_depth
            self.class_predictors.add(ConvPredictor((num_anchors * (len(self.classes) + 1))))
            self.box_predictors.add(ConvPredictor((num_anchors * 4)))
        self.bbox_decoder = NormalizedBoxCenterDecoder(stds)
        self.cls_decoder = MultiPerClassDecoder((len(self.classes) + 1), thresh=0.01)