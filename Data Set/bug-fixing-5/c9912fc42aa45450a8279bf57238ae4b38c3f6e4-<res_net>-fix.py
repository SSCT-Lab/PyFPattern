def res_net(x, y, activation=tf.nn.relu):
    'Builds a residual network.\n\n  Note that if the input tensor is 2D, it must be square in order to be\n  converted to a 4D tensor.\n\n  Borrowed structure from:\n  github.com/pkmital/tensorflow_tutorials/blob/master/10_residual_network.py\n\n  Args:\n    x: Input of the network\n    y: Output of the network\n    activation: Activation function to apply after each convolution\n\n  Returns:\n    Predictions and loss tensors.\n  '
    BottleneckGroup = namedtuple('BottleneckGroup', ['num_blocks', 'num_filters', 'bottleneck_size'])
    groups = [BottleneckGroup(3, 128, 32), BottleneckGroup(3, 256, 64), BottleneckGroup(3, 512, 128), BottleneckGroup(3, 1024, 256)]
    input_shape = x.get_shape().as_list()
    if (len(input_shape) == 2):
        ndim = int(sqrt(input_shape[1]))
        x = tf.reshape(x, [(- 1), ndim, ndim, 1])
    with tf.variable_scope('conv_layer1'):
        net = learn.ops.conv2d(x, 64, [7, 7], batch_norm=True, activation=activation, bias=False)
    net = tf.nn.max_pool(net, [1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    with tf.variable_scope('conv_layer2'):
        net = learn.ops.conv2d(net, groups[0].num_filters, [1, 1], [1, 1, 1, 1], padding='VALID', bias=True)
    for (group_i, group) in enumerate(groups):
        for block_i in range(group.num_blocks):
            name = ('group_%d/block_%d' % (group_i, block_i))
            with tf.variable_scope((name + '/conv_in')):
                conv = learn.ops.conv2d(net, group.bottleneck_size, [1, 1], [1, 1, 1, 1], padding='VALID', activation=activation, batch_norm=True, bias=False)
            with tf.variable_scope((name + '/conv_bottleneck')):
                conv = learn.ops.conv2d(conv, group.bottleneck_size, [3, 3], [1, 1, 1, 1], padding='SAME', activation=activation, batch_norm=True, bias=False)
            with tf.variable_scope((name + '/conv_out')):
                input_dim = net.get_shape()[(- 1)].value
                conv = learn.ops.conv2d(conv, input_dim, [1, 1], [1, 1, 1, 1], padding='VALID', activation=activation, batch_norm=True, bias=False)
            net = (conv + net)
        try:
            next_group = groups[(group_i + 1)]
            with tf.variable_scope(('block_%d/conv_upscale' % group_i)):
                net = learn.ops.conv2d(net, next_group.num_filters, [1, 1], [1, 1, 1, 1], bias=False, padding='SAME')
        except IndexError:
            pass
    net_shape = net.get_shape().as_list()
    net = tf.nn.avg_pool(net, ksize=[1, net_shape[1], net_shape[2], 1], strides=[1, 1, 1, 1], padding='VALID')
    net_shape = net.get_shape().as_list()
    net = tf.reshape(net, [(- 1), ((net_shape[1] * net_shape[2]) * net_shape[3])])
    return learn.models.logistic_regression(net, y)