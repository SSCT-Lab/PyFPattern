@tf_export('nn.atrous_conv2d_transpose')
def atrous_conv2d_transpose(value, filters, output_shape, rate, padding, name=None):
    'The transpose of `atrous_conv2d`.\n\n  This operation is sometimes called "deconvolution" after [Deconvolutional\n  Networks](http://www.matthewzeiler.com/pubs/cvpr2010/cvpr2010.pdf), but is\n  actually the transpose (gradient) of `atrous_conv2d` rather than an actual\n  deconvolution.\n\n  Args:\n    value: A 4-D `Tensor` of type `float`. It needs to be in the default `NHWC`\n      format. Its shape is `[batch, in_height, in_width, in_channels]`.\n    filters: A 4-D `Tensor` with the same type as `value` and shape\n      `[filter_height, filter_width, out_channels, in_channels]`. `filters`\'\n      `in_channels` dimension must match that of `value`. Atrous convolution is\n      equivalent to standard convolution with upsampled filters with effective\n      height `filter_height + (filter_height - 1) * (rate - 1)` and effective\n      width `filter_width + (filter_width - 1) * (rate - 1)`, produced by\n      inserting `rate - 1` zeros along consecutive elements across the\n      `filters`\' spatial dimensions.\n    output_shape: A 1-D `Tensor` of shape representing the output shape of the\n      deconvolution op.\n    rate: A positive int32. The stride with which we sample input values across\n      the `height` and `width` dimensions. Equivalently, the rate by which we\n      upsample the filter values by inserting zeros across the `height` and\n      `width` dimensions. In the literature, the same parameter is sometimes\n      called `input stride` or `dilation`.\n    padding: A string, either `\'VALID\'` or `\'SAME\'`. The padding algorithm.\n    name: Optional name for the returned tensor.\n\n  Returns:\n    A `Tensor` with the same type as `value`.\n\n  Raises:\n    ValueError: If input/output depth does not match `filters`\' shape, or if\n      padding is other than `\'VALID\'` or `\'SAME\'`, or if the `rate` is less\n      than one, or if the output_shape is not a tensor with 4 elements.\n  '
    with ops.name_scope(name, 'atrous_conv2d_transpose', [value, filters, output_shape]) as name:
        value = ops.convert_to_tensor(value, name='value')
        filters = ops.convert_to_tensor(filters, name='filters')
        if (not value.get_shape().dims[3].is_compatible_with(filters.get_shape()[3])):
            raise ValueError("value's input channels does not match filters' input channels, {} != {}".format(value.get_shape()[3], filters.get_shape()[3]))
        if (rate < 1):
            raise ValueError('rate {} cannot be less than one'.format(rate))
        if (rate == 1):
            return conv2d_transpose(value, filters, output_shape, strides=[1, 1, 1, 1], padding=padding, data_format='NHWC')
        output_shape_ = ops.convert_to_tensor(output_shape, name='output_shape')
        if (not output_shape_.get_shape().is_compatible_with(tensor_shape.vector(4))):
            raise ValueError('output_shape must have shape (4,), got {}'.format(output_shape_.get_shape()))
        if isinstance(output_shape, tuple):
            raise ValueError('output_shape cannot be of type tuple')
        if isinstance(output_shape, (list, np.ndarray)):
            if (not filters.get_shape().dims[2].is_compatible_with(output_shape[3])):
                raise ValueError("output_shape does not match filter's output channels, {} != {}".format(output_shape[3], filters.get_shape()[2]))
        if (padding == 'SAME'):
            if filters.get_shape().is_fully_defined():
                filter_shape = filters.get_shape().as_list()
            else:
                filter_shape = array_ops.shape(filters)
            (filter_height, filter_width) = (filter_shape[0], filter_shape[1])
            filter_height_up = (filter_height + ((filter_height - 1) * (rate - 1)))
            filter_width_up = (filter_width + ((filter_width - 1) * (rate - 1)))
            pad_height = (filter_height_up - 1)
            pad_width = (filter_width_up - 1)
            pad_top = (pad_height // 2)
            pad_bottom = (pad_height - pad_top)
            pad_left = (pad_width // 2)
            pad_right = (pad_width - pad_left)
        elif (padding == 'VALID'):
            pad_top = 0
            pad_bottom = 0
            pad_left = 0
            pad_right = 0
        else:
            raise ValueError('padding must be either VALID or SAME: {}'.format(padding))
        in_height = ((output_shape[1] + pad_top) + pad_bottom)
        in_width = ((output_shape[2] + pad_left) + pad_right)
        pad_bottom_extra = ((rate - (in_height % rate)) % rate)
        pad_right_extra = ((rate - (in_width % rate)) % rate)
        space_to_batch_pad = [[0, pad_bottom_extra], [0, pad_right_extra]]
        value = array_ops.space_to_batch(input=value, paddings=space_to_batch_pad, block_size=rate)
        input_sizes = [((rate * rate) * output_shape[0]), ((in_height + pad_bottom_extra) // rate), ((in_width + pad_right_extra) // rate), output_shape[3]]
        value = gen_nn_ops.conv2d_backprop_input(input_sizes=input_sizes, filter=filters, out_backprop=value, strides=[1, 1, 1, 1], padding='VALID', data_format='NHWC')
        batch_to_space_crop = [[pad_top, (pad_bottom + pad_bottom_extra)], [pad_left, (pad_right + pad_right_extra)]]
        return array_ops.batch_to_space(input=value, crops=batch_to_space_crop, block_size=rate)