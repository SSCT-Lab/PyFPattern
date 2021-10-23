def pool(input, window_shape, pooling_type, padding, dilation_rate=None, strides=None, name=None, data_format=None):
    'Performs an N-D pooling operation.\n\n  In the case that `data_format` does not start with "NC", computes for\n      0 <= b < batch_size,\n      0 <= x[i] < output_spatial_shape[i],\n      0 <= c < num_channels:\n\n    output[b, x[0], ..., x[N-1], c] =\n      REDUCE_{z[0], ..., z[N-1]}\n        input[b,\n              x[0] * strides[0] - pad_before[0] + dilation_rate[0]*z[0],\n              ...\n              x[N-1]*strides[N-1] - pad_before[N-1] + dilation_rate[N-1]*z[N-1],\n              c],\n\n  where the reduction function REDUCE depends on the value of `pooling_type`,\n  and pad_before is defined based on the value of `padding` as described in the\n  @{tf.nn.convolution$comment here}.\n  The reduction never includes out-of-bounds positions.\n\n  In the case that `data_format` starts with `"NC"`, the `input` and output are\n  simply transposed as follows:\n\n    pool(input, data_format, **kwargs) =\n      tf.transpose(pool(tf.transpose(input, [0] + range(2,N+2) + [1]),\n                        **kwargs),\n                   [0, N+1] + range(1, N+1))\n\n  Args:\n    input: Tensor of rank N+2, of shape\n      `[batch_size] + input_spatial_shape + [num_channels]` if data_format does\n      not start with "NC" (default), or\n      `[batch_size, num_channels] + input_spatial_shape` if data_format starts\n      with "NC".  Pooling happens over the spatial dimensions only.\n    window_shape: Sequence of N ints >= 1.\n    pooling_type: Specifies pooling operation, must be "AVG" or "MAX".\n    padding: The padding algorithm, must be "SAME" or "VALID".\n      See the @{tf.nn.convolution$comment here}\n    dilation_rate: Optional.  Dilation rate.  List of N ints >= 1.\n      Defaults to [1]*N.  If any value of dilation_rate is > 1, then all values\n      of strides must be 1.\n    strides: Optional.  Sequence of N ints >= 1.  Defaults to [1]*N.\n      If any value of strides is > 1, then all values of dilation_rate must be\n      1.\n    name: Optional. Name of the op.\n    data_format: A string or None.  Specifies whether the channel dimension of\n      the `input` and output is the last dimension (default, or if `data_format`\n      does not start with "NC"), or the second dimension (if `data_format`\n      starts with "NC").  For N=1, the valid values are "NWC" (default) and\n      "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".  For\n      N=3, the valid value is "NDHWC".\n\n  Returns:\n    Tensor of rank N+2, of shape\n      [batch_size] + output_spatial_shape + [num_channels]\n\n    if data_format is None or does not start with "NC", or\n\n      [batch_size, num_channels] + output_spatial_shape\n\n    if data_format starts with "NC",\n    where `output_spatial_shape` depends on the value of padding:\n\n    If padding = "SAME":\n      output_spatial_shape[i] = ceil(input_spatial_shape[i] / strides[i])\n    If padding = "VALID":\n      output_spatial_shape[i] =\n        ceil((input_spatial_shape[i] - (window_shape[i] - 1) * dilation_rate[i])\n             / strides[i]).\n\n  Raises:\n    ValueError: if arguments are invalid.\n\n  '
    with ops.name_scope(name, ('%s_pool' % pooling_type.lower()), [input]) as scope:
        input = ops.convert_to_tensor(input, name='input')
        num_spatial_dims = len(window_shape)
        if ((num_spatial_dims < 1) or (num_spatial_dims > 3)):
            raise ValueError('It is required that 1 <= num_spatial_dims <= 3.')
        input.get_shape().with_rank((num_spatial_dims + 2))
        (strides, dilation_rate) = _get_strides_and_dilation_rate(num_spatial_dims, strides, dilation_rate)
        if ((padding == 'SAME') and np.any((dilation_rate > 1))):
            raise ValueError('pooling with SAME padding is not implemented for dilation_rate > 1')
        if np.any((strides > window_shape)):
            raise ValueError('strides > window_shape not supported due to inconsistency between CPU and GPU implementations')
        pooling_ops = {
            ('MAX', 1): max_pool,
            ('MAX', 2): max_pool,
            ('MAX', 3): max_pool3d,
            ('AVG', 1): avg_pool,
            ('AVG', 2): avg_pool,
            ('AVG', 3): avg_pool3d,
        }
        op_key = (pooling_type, num_spatial_dims)
        if (op_key not in pooling_ops):
            raise ValueError(('%d-D %s pooling is not supported.' % (op_key[1], op_key[0])))
        if ((data_format is None) or (not data_format.startswith('NC'))):
            adjusted_window_shape = (([1] + list(window_shape)) + [1])
            adjusted_strides = (([1] + list(strides)) + [1])
            spatial_dims = range(1, (num_spatial_dims + 1))
        else:
            adjusted_window_shape = ([1, 1] + list(window_shape))
            adjusted_strides = ([1, 1] + list(strides))
            spatial_dims = range(2, (num_spatial_dims + 2))
        if (num_spatial_dims == 3):
            if ((data_format is not None) and (data_format != 'NDHWC')):
                raise ValueError('data_format must be "NDHWC".')
            data_format_kwargs = dict()
        elif (num_spatial_dims == 1):
            if ((data_format is None) or (data_format == 'NWC')):
                data_format_kwargs = dict(data_format='NHWC')
            elif (data_format == 'NCW'):
                data_format_kwargs = dict(data_format='NCHW')
            else:
                raise ValueError('data_format must be either "NWC" or "NCW".')
            adjusted_window_shape = ([1] + adjusted_window_shape)
            adjusted_strides = ([1] + adjusted_strides)
        else:
            data_format_kwargs = dict(data_format=data_format)

        def op(converted_input, _, converted_padding):
            if (num_spatial_dims == 1):
                converted_input = array_ops.expand_dims(converted_input, spatial_dims[0])
            result = pooling_ops[op_key](converted_input, adjusted_window_shape, adjusted_strides, converted_padding, name=scope, **data_format_kwargs)
            if (num_spatial_dims == 1):
                result = array_ops.squeeze(result, [spatial_dims[0]])
            return result
        return with_space_to_batch(input=input, dilation_rate=dilation_rate, padding=padding, op=op, spatial_dims=spatial_dims, filter_shape=window_shape)