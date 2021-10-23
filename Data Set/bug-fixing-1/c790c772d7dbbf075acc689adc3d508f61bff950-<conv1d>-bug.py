

def conv1d(value, filters, stride, padding, use_cudnn_on_gpu=None, data_format=None, name=None):
    'Computes a 1-D convolution given 3-D input and filter tensors.\n\n  Given an input tensor of shape\n    [batch, in_width, in_channels]\n  if data_format is "NHWC", or\n    [batch, in_channels, in_width]\n  if data_format is "NCHW",\n  and a filter / kernel tensor of shape\n  [filter_width, in_channels, out_channels], this op reshapes\n  the arguments to pass them to conv2d to perform the equivalent\n  convolution operation.\n\n  Internally, this op reshapes the input tensors and invokes `tf.nn.conv2d`.\n  For example, if `data_format` does not start with "NC", a tensor of shape\n    [batch, in_width, in_channels]\n  is reshaped to\n    [batch, 1, in_width, in_channels],\n  and the filter is reshaped to\n    [1, filter_width, in_channels, out_channels].\n  The result is then reshaped back to\n    [batch, out_width, out_channels]\n  (where out_width is a function of the stride and padding as in conv2d) and\n  returned to the caller.\n\n  Args:\n    value: A 3D `Tensor`.  Must be of type `float32` or `float64`.\n    filters: A 3D `Tensor`.  Must have the same type as `input`.\n    stride: An `integer`.  The number of entries by which\n      the filter is moved right at each step.\n    padding: \'SAME\' or \'VALID\'\n    use_cudnn_on_gpu: An optional `bool`.  Defaults to `True`.\n    data_format: An optional `string` from `"NHWC", "NCHW"`.  Defaults\n      to `"NHWC"`, the data is stored in the order of\n      [batch, in_width, in_channels].  The `"NCHW"` format stores\n      data as [batch, in_channels, in_width].\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor`.  Has the same type as input.\n\n  Raises:\n    ValueError: if `data_format` is invalid.\n  '
    with ops.name_scope(name, 'conv1d', [value, filters]) as name:
        if ((data_format is None) or (data_format == 'NHWC')):
            data_format = 'NHWC'
            spatial_start_dim = 1
            strides = [1, 1, stride, 1]
        elif (data_format == 'NCHW'):
            spatial_start_dim = 2
            strides = [1, 1, 1, stride]
        else:
            raise ValueError('data_format must be "NHWC" or "NCHW".')
        value = array_ops.expand_dims(value, spatial_start_dim)
        filters = array_ops.expand_dims(filters, 0)
        result = gen_nn_ops.conv2d(value, filters, strides, padding, use_cudnn_on_gpu=use_cudnn_on_gpu, data_format=data_format)
        return array_ops.squeeze(result, [spatial_start_dim])
