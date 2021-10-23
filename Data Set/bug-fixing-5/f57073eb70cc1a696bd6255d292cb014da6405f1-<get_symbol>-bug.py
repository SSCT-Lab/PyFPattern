def get_symbol(num_classes=1000, **kwargs):
    data = mx.sym.Variable('data')
    conv1 = ConvFactory(data, 64, kernel=(7, 7), stride=(2, 2), pad=(3, 3), name='conv1')
    pool1 = mx.sym.Pooling(conv1, kernel=(3, 3), stride=(2, 2), pool_type='max')
    conv2 = ConvFactory(pool1, 64, kernel=(1, 1), stride=(1, 1), name='conv2')
    conv3 = ConvFactory(conv2, 192, kernel=(3, 3), stride=(1, 1), pad=(1, 1), name='conv3')
    pool3 = mx.sym.Pooling(conv3, kernel=(3, 3), stride=(2, 2), pool_type='max')
    in3a = InceptionFactory(pool3, 64, 96, 128, 16, 32, 'max', 32, name='in3a')
    in3b = InceptionFactory(in3a, 128, 128, 192, 32, 96, 'max', 64, name='in3b')
    pool4 = mx.sym.Pooling(in3b, kernel=(3, 3), stride=(2, 2), pool_type='max')
    in4a = InceptionFactory(pool4, 192, 96, 208, 16, 48, 'max', 64, name='in4a')
    in4b = InceptionFactory(in4a, 160, 112, 224, 24, 64, 'max', 64, name='in4b')
    in4c = InceptionFactory(in4b, 128, 128, 256, 24, 64, 'max', 64, name='in4c')
    in4d = InceptionFactory(in4c, 112, 144, 288, 32, 64, 'max', 64, name='in4d')
    in4e = InceptionFactory(in4d, 256, 160, 320, 32, 128, 'max', 128, name='in4e')
    pool5 = mx.sym.Pooling(in4e, kernel=(3, 3), stride=(2, 2), pool_type='max')
    in5a = InceptionFactory(pool5, 256, 160, 320, 32, 128, 'max', 128, name='in5a')
    in5b = InceptionFactory(in5a, 384, 192, 384, 48, 128, 'max', 128, name='in5b')
    pool6 = mx.sym.Pooling(in5b, kernel=(7, 7), stride=(1, 1), pool_type='avg')
    flatten = mx.sym.Flatten(data=pool6)
    fc1 = mx.sym.FullyConnected(data=flatten, num_hidden=num_classes)
    softmax = mx.symbol.SoftmaxOutput(data=fc1, name='softmax')
    return softmax