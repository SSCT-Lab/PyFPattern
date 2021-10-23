

def conv2d_transpose(x, kernel, output_shape, strides=(1, 1), padding='valid', data_format=None):
    '2D deconvolution (transposed convolution).\n\n    # Arguments\n        kernel: kernel tensor.\n        output_shape: desired dimensions of output.\n        strides: strides tuple.\n        padding: string, "same" or "valid".\n        data_format: "channels_last" or "channels_first".\n            Whether to use Theano or TensorFlow data format\n        in inputs/kernels/outputs.\n    '
    flip_filters = False
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError(('Unknown data_format ' + data_format))
    if (data_format == 'channels_last'):
        output_shape = (output_shape[0], output_shape[3], output_shape[1], output_shape[2])
    if hasattr(kernel, '_keras_shape'):
        kernel_shape = kernel._keras_shape
    else:
        kernel_shape = kernel.eval().shape
    kernel_shape = _preprocess_conv2d_filter_shape(kernel_shape, data_format)
    x = _preprocess_conv2d_input(x, data_format)
    kernel = _preprocess_conv2d_kernel(kernel, data_format)
    th_padding = _preprocess_padding(padding)
    op = T.nnet.abstract_conv.AbstractConv2d_gradInputs(imshp=None, kshp=kernel_shape, subsample=strides, border_mode=th_padding, filter_flip=(not flip_filters))
    conv_out = op(kernel, x, output_shape[2:])
    conv_out = _postprocess_conv2d_output(conv_out, x, padding, kernel_shape, strides, data_format)
    return conv_out
