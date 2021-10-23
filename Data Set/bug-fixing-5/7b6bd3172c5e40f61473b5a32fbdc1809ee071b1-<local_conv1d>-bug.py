def local_conv1d(inputs, kernel, kernel_size, strides, data_format=None):
    'Apply 1D conv with un-shared weights.\n\n    # Arguments\n        inputs: 3D tensor with shape: (batch_size, steps, input_dim)\n        kernel: the unshared weight for convolution,\n                with shape (output_length, feature_dim, filters)\n        kernel_size: a tuple of a single integer,\n                     specifying the length of the 1D convolution window\n        strides: a tuple of a single integer,\n                 specifying the stride length of the convolution\n        data_format: the data format, channels_first or channels_last\n\n    # Returns\n        the tensor after 1d conv with un-shared weights, with shape (batch_size, output_lenght, filters)\n\n    # Raises\n        ValueError: if `data_format` is neither `channels_last` or `channels_first`.\n    '
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError(('Unknown data_format ' + str(data_format)))
    stride = strides[0]
    kernel_shape = int_shape(kernel)
    (output_length, feature_dim, filters) = kernel_shape
    xs = []
    for i in range(output_length):
        slice_length = slice((i * stride), ((i * stride) + kernel_size[0]))
        xs.append(reshape(inputs[:, slice_length, :], (1, (- 1), feature_dim)))
    x_aggregate = concatenate(xs, axis=0)
    output = batch_dot(x_aggregate, kernel)
    return permute_dimensions(output, (1, 0, 2))