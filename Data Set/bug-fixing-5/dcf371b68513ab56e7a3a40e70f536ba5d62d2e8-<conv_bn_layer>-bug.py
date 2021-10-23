def conv_bn_layer(input, num_filters, filter_size, stride=1, groups=1, act=None):
    conv = fluid.layers.conv2d(input=input, num_filters=num_filters, filter_size=filter_size, stride=stride, padding=((filter_size - 1) // 2), groups=groups, act=None, bias_attr=False)
    return (conv if remove_bn else fluid.layers.batch_norm(input=conv, act=act, momentum=0.1))