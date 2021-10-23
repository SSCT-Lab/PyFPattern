

def constant(value, dtype=None, shape=None, name='Const', verify_shape=False):
    'Creates a constant tensor.\n\n  The resulting tensor is populated with values of type `dtype`, as\n  specified by arguments `value` and (optionally) `shape` (see examples\n  below).\n\n  The argument `value` can be a constant value, or a list of values of type\n  `dtype`. If `value` is a list, then the length of the list must be less\n  than or equal to the number of elements implied by the `shape` argument (if\n  specified). In the case where the list length is less than the number of\n  elements specified by `shape`, the last element in the list will be used\n  to fill the remaining entries.\n\n  The argument `shape` is optional. If present, it specifies the dimensions of\n  the resulting tensor. If not present, the shape of `value` is used.\n\n  If the argument `dtype` is not specified, then the type is inferred from\n  the type of `value`.\n\n  For example:\n\n  ```python\n  # Constant 1-D Tensor populated with value list.\n  tensor = tf.constant([1, 2, 3, 4, 5, 6, 7]) => [1 2 3 4 5 6 7]\n\n  # Constant 2-D tensor populated with scalar value -1.\n  tensor = tf.constant(-1.0, shape=[2, 3]) => [[-1. -1. -1.]\n                                               [-1. -1. -1.]]\n  ```\n\n  Args:\n    value:          A constant value (or list) of output type `dtype`.\n\n    dtype:          The type of the elements of the resulting tensor.\n\n    shape:          Optional dimensions of resulting tensor.\n\n    name:           Optional name for the tensor.\n\n    verify_shape:   Boolean that enables verification of a shape of values.\n\n  Returns:\n    A Constant Tensor.\n\n  Raises:\n    TypeError if shape is incorrectly specified or unsupported.\n  '
    if (not context.in_graph_mode()):
        if (shape is None):
            return convert_to_eager_tensor(value, dtype)
        t = convert_to_eager_tensor(value, dtype)
        shape = tensor_shape.as_shape(shape)
        if (shape == t.shape):
            return t
        if verify_shape:
            raise TypeError(("Expected Tensor's shape: %s, got %s." % (tuple(shape), tuple(t.shape))))
        num_t = t.shape.num_elements()
        if (num_t == shape.num_elements()):
            return _eager_reshape(t, shape.as_list())
        if (num_t == 1):
            if (t.dtype == dtypes.bool):
                with ops.device('/device:CPU:0'):
                    x = _eager_fill(shape.as_list(), t.as_cpu_tensor())
                return _eager_identity(x)
            else:
                return _eager_fill(shape.as_list(), t)
        raise TypeError(('Eager execution of tf.constant with unsupported shape (value has %d elements, shape is %s with %d elements).' % (num_t, shape, shape.num_elements())))
    g = ops.get_default_graph()
    tensor_value = attr_value_pb2.AttrValue()
    tensor_value.tensor.CopyFrom(tensor_util.make_tensor_proto(value, dtype=dtype, shape=shape, verify_shape=verify_shape))
    dtype_value = attr_value_pb2.AttrValue(type=tensor_value.tensor.dtype)
    const_tensor = g.create_op('Const', [], [dtype_value.type], attrs={
        'value': tensor_value,
        'dtype': dtype_value,
    }, name=name).outputs[0]
    return const_tensor
