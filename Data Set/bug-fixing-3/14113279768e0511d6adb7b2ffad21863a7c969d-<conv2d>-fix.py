def conv2d(x, kernel, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1)):
    '2D convolution.\n\n    # Arguments\n        kernel: kernel tensor.\n        strides: strides tuple.\n        padding: string, "same" or "valid".\n        data_format: "channels_last" or "channels_first".\n            Whether to use Theano or TensorFlow data format\n        in inputs/kernels/outputs.\n    '
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError('Unknown data_format ', data_format)
    image_shape = _preprocess_conv2d_image_shape(int_shape(x), data_format)
    kernel_shape = int_shape(kernel)
    if (kernel_shape is None):
        kernel_shape = kernel.eval().shape
    kernel_shape = _preprocess_conv2d_filter_shape(kernel_shape, data_format)
    x = _preprocess_conv2d_input(x, data_format)
    kernel = _preprocess_conv2d_kernel(kernel, data_format)
    th_padding = _preprocess_padding(padding)
    conv_out = T.nnet.conv2d(x, kernel, border_mode=th_padding, subsample=strides, input_shape=image_shape, filter_shape=kernel_shape, filter_dilation=dilation_rate)
    conv_out = _postprocess_conv2d_output(conv_out, x, padding, kernel_shape, strides, data_format)
    return conv_out