def size_internal(input, name=None, optimize=True, out_type=dtypes.int32):
    'Returns the size of a tensor.\n\n  Args:\n    input: A `Tensor` or `SparseTensor`.\n    name: A name for the operation (optional).\n    optimize: if true, encode the size as a constant when possible.\n    out_type: (Optional) The specified non-quantized numeric output type\n      of the operation. Defaults to `tf.int32`.\n\n  Returns:\n    A `Tensor` of type `out_type`. Defaults to `tf.int32`.\n  '
    with ops.name_scope(name, 'Size', [input]) as name:
        if isinstance(input, (sparse_tensor.SparseTensor, sparse_tensor.SparseTensorValue)):
            return gen_math_ops._prod(gen_math_ops.cast(input.dense_shape, out_type), 0, name=name)
        else:
            input_tensor = ops.convert_to_tensor(input)
            input_shape = input_tensor.get_shape()
            if (optimize and input_shape.is_fully_defined()):
                return constant(input_shape.num_elements(), out_type, name=name)
            return gen_array_ops.size(input, name=name, out_type=out_type)