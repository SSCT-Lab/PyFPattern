def conv1d(x, kernel, strides=1, padding='valid', data_format=None, dilation_rate=1):
    '1D convolution.\n\n    # Arguments\n        kernel: kernel tensor.\n        strides: stride integer.\n        padding: string, `"same"`, `"causal"` or `"valid"`.\n        data_format: string, one of "channels_last", "channels_first"\n        dilation_rate: integer.\n    '
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError('Unknown data_format ', data_format)
    kernel_shape = int_shape(kernel)
    if (padding == 'causal'):
        if (not kernel_shape):
            raise AttributeError('Causal padding requires kernel._keras_shape set.')
        left_pad = (dilation_rate * (kernel_shape[0] - 1))
        x = temporal_padding(x, (left_pad, 0))
        padding = 'valid'
    shape = int_shape(x)
    if (data_format == 'channels_last'):
        x = expand_dims(x, 2)
        if (shape is not None):
            x._keras_shape = (shape[0], shape[1], 1, shape[2])
    else:
        x = expand_dims(x, 3)
        if (shape is not None):
            x._keras_shape = (shape[0], shape[1], shape[2], 1)
    dilation_rate = (dilation_rate, 1)
    strides = (strides, 1)
    kernel = expand_dims(kernel, 1)
    output = conv2d(x, kernel, strides=strides, padding=padding, data_format=data_format, dilation_rate=dilation_rate)
    if (data_format == 'channels_last'):
        output = squeeze(output, 2)
    else:
        output = squeeze(output, 3)
    return output