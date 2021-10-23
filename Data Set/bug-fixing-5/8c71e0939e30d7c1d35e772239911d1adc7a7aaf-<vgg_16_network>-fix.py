def vgg_16_network(input_image, num_channels, num_classes=1000):
    "\n    Same model from https://gist.github.com/ksimonyan/211839e770f7b538e2d8\n\n    :param num_classes: number of class.\n    :type num_classes: int\n    :param input_image: input layer.\n    :type input_image: LayerOutput\n    :param num_channels: input channels num.\n    :type num_channels: int\n    :return: layer's output\n    :rtype: LayerOutput\n    "
    tmp = img_conv_group(input=input_image, num_channels=num_channels, conv_padding=1, conv_num_filter=[64, 64], conv_filter_size=3, conv_act=ReluActivation(), pool_size=2, pool_stride=2, pool_type=MaxPooling())
    tmp = img_conv_group(input=tmp, conv_num_filter=[128, 128], conv_padding=1, conv_filter_size=3, conv_act=ReluActivation(), pool_stride=2, pool_type=MaxPooling(), pool_size=2)
    tmp = img_conv_group(input=tmp, conv_num_filter=[256, 256, 256], conv_padding=1, conv_filter_size=3, conv_act=ReluActivation(), pool_stride=2, pool_type=MaxPooling(), pool_size=2)
    tmp = img_conv_group(input=tmp, conv_num_filter=[512, 512, 512], conv_padding=1, conv_filter_size=3, conv_act=ReluActivation(), pool_stride=2, pool_type=MaxPooling(), pool_size=2)
    tmp = img_conv_group(input=tmp, conv_num_filter=[512, 512, 512], conv_padding=1, conv_filter_size=3, conv_act=ReluActivation(), pool_stride=2, pool_type=MaxPooling(), pool_size=2)
    tmp = fc_layer(input=tmp, size=4096, act=ReluActivation(), layer_attr=ExtraAttr(drop_rate=0.5))
    tmp = fc_layer(input=tmp, size=4096, act=ReluActivation(), layer_attr=ExtraAttr(drop_rate=0.5))
    return fc_layer(input=tmp, size=num_classes, act=SoftmaxActivation())