

def conv2d_transpose(value, filter, output_shape, strides, padding='SAME', data_format='NHWC', name=None):
    'The transpose of `conv2d`.\n\n  This operation is sometimes called "deconvolution" after [Deconvolutional\n  Networks](http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf), but is\n  actually the transpose (gradient) of `conv2d` rather than an actual\n  deconvolution.\n\n  Args:\n    value: A 4-D `Tensor` of type `float` and shape\n      `[batch, height, width, in_channels]` for `NHWC` data format or\n      `[batch, in_channels, height, width]` for `NCHW` data format.\n    filter: A 4-D `Tensor` with the same type as `value` and shape\n      `[height, width, output_channels, in_channels]`.  `filter`\'s\n      `in_channels` dimension must match that of `value`.\n    output_shape: A 1-D `Tensor` representing the output shape of the\n      deconvolution op.\n    strides: A list of ints. The stride of the sliding window for each\n      dimension of the input tensor.\n    padding: A string, either `\'VALID\'` or `\'SAME\'`. The padding algorithm.\n      See the @{tf.nn.convolution$comment here}\n    data_format: A string. \'NHWC\' and \'NCHW\' are supported.\n    name: Optional name for the returned tensor.\n\n  Returns:\n    A `Tensor` with the same type as `value`.\n\n  Raises:\n    ValueError: If input/output depth does not match `filter`\'s shape, or if\n      padding is other than `\'VALID\'` or `\'SAME\'`.\n  '
    with ops.name_scope(name, 'conv2d_transpose', [value, filter, output_shape]) as name:
        if (data_format not in ('NCHW', 'NHWC')):
            raise ValueError('data_format has to be either NCHW or NHWC.')
        value = ops.convert_to_tensor(value, name='value')
        filter = ops.convert_to_tensor(filter, name='filter')
        axis = (3 if (data_format == 'NHWC') else 1)
        if (not value.get_shape()[axis].is_compatible_with(filter.get_shape()[3])):
            raise ValueError("input channels does not match filter's input channels, {} != {}".format(value.get_shape()[axis], filter.get_shape()[3]))
        output_shape_ = ops.convert_to_tensor(output_shape, name='output_shape')
        if (not output_shape_.get_shape().is_compatible_with(tensor_shape.vector(4))):
            raise ValueError('output_shape must have shape (4,), got {}'.format(output_shape_.get_shape()))
        if isinstance(output_shape, (list, np.ndarray)):
            if (not filter.get_shape()[2].is_compatible_with(output_shape[axis])):
                raise ValueError("output_shape does not match filter's output channels, {} != {}".format(output_shape[axis], filter.get_shape()[2]))
        if ((padding != 'VALID') and (padding != 'SAME')):
            raise ValueError('padding must be either VALID or SAME: {}'.format(padding))
        return gen_nn_ops.conv2d_backprop_input(input_sizes=output_shape_, filter=filter, out_backprop=value, strides=strides, padding=padding, data_format=data_format, name=name)
