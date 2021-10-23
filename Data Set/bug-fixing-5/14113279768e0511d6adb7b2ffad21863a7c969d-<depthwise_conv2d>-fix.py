def depthwise_conv2d(x, depthwise_kernel, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1)):
    '2D convolution with separable filters.\n\n    # Arguments\n        x: input tensor\n        depthwise_kernel: convolution kernel for the depthwise convolution.\n        strides: strides tuple (length 2).\n        padding: string, `"same"` or `"valid"`.\n        data_format: string, `"channels_last"` or `"channels_first"`.\n        dilation_rate: tuple of integers,\n            dilation rates for the separable convolution.\n\n    # Returns\n        Output tensor.\n\n    # Raises\n        ValueError: if `data_format` is neither `"channels_last"` or `"channels_first"`.\n    '
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError('Unknown data_format ', data_format)
    image_shape = _preprocess_conv2d_image_shape(int_shape(x), data_format)
    depthwise_kernel_shape = int_shape(depthwise_kernel)
    if (depthwise_kernel_shape is None):
        depthwise_kernel_shape = depthwise_kernel.eval().shape
    depthwise_kernel_shape = _preprocess_conv2d_filter_shape(depthwise_kernel_shape, data_format)
    x = _preprocess_conv2d_input(x, data_format)
    depthwise_kernel = _preprocess_conv2d_kernel(depthwise_kernel, data_format)
    th_padding = _preprocess_padding(padding)
    input_depth = depthwise_kernel_shape[1]
    output_depth = depthwise_kernel_shape[0]
    depthwise_kernel_shape = (((input_depth * output_depth), 1) + depthwise_kernel_shape[2:])
    depthwise_kernel = depthwise_kernel.dimshuffle((1, 0, 2, 3))
    depthwise_kernel = reshape(depthwise_kernel, depthwise_kernel_shape)
    depthwise_kernel = depthwise_kernel[:, :, ::(- 1), ::(- 1)]
    conv_out = T.nnet.conv2d(x, depthwise_kernel, border_mode=th_padding, subsample=strides, input_shape=image_shape, filter_shape=depthwise_kernel_shape, filter_dilation=dilation_rate, num_groups=input_depth)
    conv_out = _postprocess_conv2d_output(conv_out, x, padding, depthwise_kernel_shape, strides, data_format)
    return conv_out