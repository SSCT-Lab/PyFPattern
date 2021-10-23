

@tf_export('nn.convolution')
def convolution(input, filter, padding, strides=None, dilation_rate=None, name=None, data_format=None):
    'Computes sums of N-D convolutions (actually cross-correlation).\n\n  This also supports either output striding via the optional `strides` parameter\n  or atrous convolution (also known as convolution with holes or dilated\n  convolution, based on the French word "trous" meaning holes in English) via\n  the optional `dilation_rate` parameter.  Currently, however, output striding\n  is not supported for atrous convolutions.\n\n  Specifically, in the case that `data_format` does not start with "NC", given\n  a rank (N+2) `input` Tensor of shape\n\n    [num_batches,\n     input_spatial_shape[0],\n     ...,\n     input_spatial_shape[N-1],\n     num_input_channels],\n\n  a rank (N+2) `filter` Tensor of shape\n\n    [spatial_filter_shape[0],\n     ...,\n     spatial_filter_shape[N-1],\n     num_input_channels,\n     num_output_channels],\n\n  an optional `dilation_rate` tensor of shape [N] (defaulting to [1]*N)\n  specifying the filter upsampling/input downsampling rate, and an optional list\n  of N `strides` (defaulting [1]*N), this computes for each N-D spatial output\n  position (x[0], ..., x[N-1]):\n\n  ```\n    output[b, x[0], ..., x[N-1], k] =\n        sum_{z[0], ..., z[N-1], q}\n            filter[z[0], ..., z[N-1], q, k] *\n            padded_input[b,\n                         x[0]*strides[0] + dilation_rate[0]*z[0],\n                         ...,\n                         x[N-1]*strides[N-1] + dilation_rate[N-1]*z[N-1],\n                         q]\n  ```\n  where b is the index into the batch, k is the output channel number, q is the\n  input channel number, and z is the N-D spatial offset within the filter. Here,\n  `padded_input` is obtained by zero padding the input using an effective\n  spatial filter shape of `(spatial_filter_shape-1) * dilation_rate + 1` and\n  output striding `strides` as described in the\n  @{tf.nn.convolution$comment here}.\n\n  In the case that `data_format` does start with `"NC"`, the `input` and output\n  (but not the `filter`) are simply transposed as follows:\n\n    convolution(input, data_format, **kwargs) =\n      tf.transpose(convolution(tf.transpose(input, [0] + range(2,N+2) + [1]),\n                               **kwargs),\n                   [0, N+1] + range(1, N+1))\n\n  It is required that 1 <= N <= 3.\n\n  Args:\n    input: An N-D `Tensor` of type `T`, of shape\n      `[batch_size] + input_spatial_shape + [in_channels]` if data_format does\n      not start with "NC" (default), or\n      `[batch_size, in_channels] + input_spatial_shape` if data_format starts\n      with "NC".\n    filter: An N-D `Tensor` with the same type as `input` and shape\n      `spatial_filter_shape + [in_channels, out_channels]`.\n    padding: A string, either `"VALID"` or `"SAME"`. The padding algorithm.\n    strides: Optional.  Sequence of N ints >= 1.  Specifies the output stride.\n      Defaults to [1]*N.  If any value of strides is > 1, then all values of\n      dilation_rate must be 1.\n    dilation_rate: Optional.  Sequence of N ints >= 1.  Specifies the filter\n      upsampling/input downsampling rate.  In the literature, the same parameter\n      is sometimes called `input stride` or `dilation`.  The effective filter\n      size used for the convolution will be `spatial_filter_shape +\n      (spatial_filter_shape - 1) * (rate - 1)`, obtained by inserting\n      (dilation_rate[i]-1) zeros between consecutive elements of the original\n      filter in each spatial dimension i.  If any value of dilation_rate is > 1,\n      then all values of strides must be 1.\n    name: Optional name for the returned tensor.\n    data_format: A string or None.  Specifies whether the channel dimension of\n      the `input` and output is the last dimension (default, or if `data_format`\n      does not start with "NC"), or the second dimension (if `data_format`\n      starts with "NC").  For N=1, the valid values are "NWC" (default) and\n      "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".\n      For N=3, the valid values are "NDHWC" (default) and "NCDHW".\n\n  Returns:\n    A `Tensor` with the same type as `input` of shape\n\n        `[batch_size] + output_spatial_shape + [out_channels]`\n\n    if data_format is None or does not start with "NC", or\n\n        `[batch_size, out_channels] + output_spatial_shape`\n\n    if data_format starts with "NC",\n    where `output_spatial_shape` depends on the value of `padding`.\n\n    If padding == "SAME":\n      output_spatial_shape[i] = ceil(input_spatial_shape[i] / strides[i])\n\n    If padding == "VALID":\n      output_spatial_shape[i] =\n        ceil((input_spatial_shape[i] -\n              (spatial_filter_shape[i]-1) * dilation_rate[i])\n             / strides[i]).\n\n  Raises:\n    ValueError: If input/output depth does not match `filter` shape, if padding\n      is other than `"VALID"` or `"SAME"`, or if data_format is invalid.\n\n  '
    with ops.name_scope(name, 'convolution', [input, filter]) as name:
        input = ops.convert_to_tensor(input, name='input')
        input_shape = input.get_shape()
        filter = ops.convert_to_tensor(filter, name='filter')
        filter_shape = filter.get_shape()
        op = Convolution(input_shape, filter_shape, padding, strides=strides, dilation_rate=dilation_rate, name=name, data_format=data_format)
        return op(input, filter)
