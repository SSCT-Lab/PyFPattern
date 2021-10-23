def conv1d(x, kernel, strides=1, padding='valid', data_format=None, dilation_rate=1):
    '1D convolution.\n\n    # Arguments\n        x: Tensor or variable.\n        kernel: kernel tensor.\n        strides: stride integer.\n        padding: string, `"same"`, `"causal"` or `"valid"`.\n        data_format: string, `"channels_last"` or `"channels_first"`.\n        dilation_rate: integer dilate rate.\n\n    # Returns\n        A tensor, result of 1D convolution.\n    '
    kernel_shape = kernel.get_shape().as_list()
    if (padding == 'causal'):
        left_pad = (dilation_rate * (kernel_shape[0] - 1))
        x = temporal_padding(x, (left_pad, 0))
        padding = 'valid'
    padding = _preprocess_padding(padding)
    if (data_format == 'channels_last'):
        tf_data_format = 'NWC'
    else:
        tf_data_format = 'NCW'
    x = tf.nn.convolution(input=x, filter=kernel, dilation_rate=(dilation_rate,), strides=(strides,), padding=padding, data_format=tf_data_format)
    return x