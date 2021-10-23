

@tf_export('nn.bias_add')
def bias_add(value, bias, data_format=None, name=None):
    "Adds `bias` to `value`.\n\n  This is (mostly) a special case of `tf.add` where `bias` is restricted to 1-D.\n  Broadcasting is supported, so `value` may have any number of dimensions.\n  Unlike `tf.add`, the type of `bias` is allowed to differ from `value` in the\n  case where both types are quantized.\n\n  Args:\n    value: A `Tensor` with type `float`, `double`, `int64`, `int32`, `uint8`,\n      `int16`, `int8`, `complex64`, or `complex128`.\n    bias: A 1-D `Tensor` with size matching the channel dimension of `value`.\n      Must be the same type as `value` unless `value` is a quantized type,\n      in which case a different quantized type may be used.\n    data_format: A string. 'N...C' and 'NC...' are supported.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` with the same type as `value`.\n  "
    with ops.name_scope(name, 'BiasAdd', [value, bias]) as name:
        if (data_format is not None):
            if data_format.startswith('NC'):
                data_format = 'NCHW'
            elif (data_format.startswith('N') and data_format.endswith('C')):
                data_format = 'NHWC'
            else:
                raise ValueError('data_format must be of the form `N...C` or `NC...`')
        if (not context.executing_eagerly()):
            value = ops.convert_to_tensor(value, name='input')
            bias = ops.convert_to_tensor(bias, dtype=value.dtype, name='bias')
        return gen_nn_ops.bias_add(value, bias, data_format=data_format, name=name)
