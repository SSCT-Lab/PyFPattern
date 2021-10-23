

def export(model, args, directory=None, export_params=True, graph_name='Graph'):
    "(Experimental) Export a computational graph as Caffe format.\n\n    Args:\n        model (~chainer.Chain): The model object you want to export in ONNX\n            format. It should have :meth:`__call__` method because the second\n            argment ``args`` is directly given to the model by the ``()``\n            accessor.\n        args (list of ~chainer.Variable): The argments which are given to the\n            model directly.\n        directory (str): The directory used for saving the resulting Caffe\n            model. If None, nothing is saved to the disk.\n        export_params (bool): If True, this function exports all the parameters\n            included in the given model at the same time. If False, the\n            exported Caffe model doesn't include any parameter values.\n        graph_name (str): A string to be used for the ``name`` field of the\n            graph in the exported Caffe model.\n\n    .. note::\n        Currently, this function supports networks that created by following\n        layer functions.\n\n        - :func:`~chainer.functions.linear`\n        - :func:`~chainer.functions.convolution_2d`\n        - :func:`~chainer.functions.deconvolution_2d`\n        - :func:`~chainer.functions.max_pooling_2d`\n        - :func:`~chainer.functions.average_pooling_2d`\n        - :func:`~chainer.functions.batch_normalization`\n        - :func:`~chainer.functions.local_response_normalization`\n        - :func:`~chainer.functions.relu`\n        - :func:`~chainer.functions.concat`\n        - :func:`~chainer.functions.softmax`\n        - :func:`~chainer.functions.reshape`\n        - :func:`~chainer.functions.add`\n\n        This function can export at least following networks.\n\n        - GoogLeNet\n        - ResNet\n        - VGG\n\n        And, this function use testing (evaluation) mode.\n\n    .. admonition:: Example\n\n       >>> from chainer.exporters import caffe\n       >>>\n       >>> class Model(chainer.Chain):\n       ...    def __init__(self):\n       ...        super(Model, self).__init__()\n       ...        with self.init_scope():\n       ...            self.l1 = L.Convolution2D(None, 1, 1, 1, 0)\n       ...            self.b2 = L.BatchNormalization(1)\n       ...            self.l3 = L.Linear(None, 1)\n       ...\n       ...    def __call__(self, x):\n       ...        h = F.relu(self.l1(x))\n       ...        h = self.b2(h)\n       ...        return self.l3(h)\n       ...\n       >>> x = chainer.Variable(np.zeros((1, 10, 10, 10), np.float32))\n       >>> caffe.export(Model(), [x], None, True, 'test')\n\n    "
    utils.experimental('chainer.exporters.caffe.export')
    assert isinstance(args, (tuple, list))
    if (len(args) != 1):
        raise NotImplementedError()
    for i in args:
        assert isinstance(i, variable.Variable)
    with function.force_backprop_mode(), chainer.using_config('train', False):
        output = model(*args)
    if isinstance(output, variable.Variable):
        output = [output]
    assert isinstance(output, (tuple, list))
    for i in output:
        assert isinstance(i, variable.Variable)
    prototxt = None
    caffemodel = None
    if (directory is not None):
        prototxt = os.path.join(directory, 'chainer_model.prototxt')
        if export_params:
            caffemodel = os.path.join(directory, 'chainer_model.caffemodel')
    retriever = _RetrieveAsCaffeModel(prototxt, caffemodel)
    retriever(graph_name, args, output)
