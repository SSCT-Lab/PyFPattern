def read_caffemodel(prototxt_fname, caffemodel_fname):
    'Return a caffe_pb2.NetParameter object that defined in a binary\n    caffemodel file\n    '
    if use_caffe:
        caffe.set_mode_cpu()
        net = caffe.Net(prototxt_fname, caffemodel_fname, caffe.TEST)
        layer_names = net._layer_names
        layers = net.layers
        return (layers, layer_names)
    else:
        proto = caffe_pb2.NetParameter()
        with open(fname, 'rb') as f:
            proto.ParseFromString(f.read())
        return (get_layers(proto), None)