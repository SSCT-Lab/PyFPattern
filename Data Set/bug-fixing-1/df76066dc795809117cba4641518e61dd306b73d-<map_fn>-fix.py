

def map_fn(fn, elems, dtype=None, parallel_iterations=10, back_prop=True, swap_memory=False, infer_shape=True, name=None):
    'map on the list of tensors unpacked from `elems` on dimension 0.\n\n  The simplest version of `map_fn` repeatedly applies the callable `fn` to a\n  sequence of elements from first to last. The elements are made of the\n  tensors unpacked from `elems`. `dtype` is the data type of the return\n  value of `fn`. Users must provide `dtype` if it is different from\n  the data type of `elems`.\n\n  Suppose that `elems` is unpacked into `values`, a list of tensors. The shape\n  of the result tensor is `[values.shape[0]] + fn(values[0]).shape`.\n\n  This method also allows multi-arity `elems` and output of `fn`.  If `elems`\n  is a (possibly nested) list or tuple of tensors, then each of these tensors\n  must have a matching first (unpack) dimension.  The signature of `fn` may\n  match the structure of `elems`.  That is, if `elems` is\n  `(t1, [t2, t3, [t4, t5]])`, then an appropriate signature for `fn` is:\n  `fn = lambda (t1, [t2, t3, [t4, t5]]):`.\n\n  Furthermore, `fn` may emit a different structure than its input.  For example,\n  `fn` may look like: `fn = lambda t1: return (t1 + 1, t1 - 1)`.  In this case,\n  the `dtype` parameter is not optional: `dtype` must be a type or (possibly\n  nested) tuple of types matching the output of `fn`.\n\n  To apply a functional operation to the nonzero elements of a SparseTensor\n  one of the following methods is recommended. First, if the function is\n  expressible as TensorFlow ops, use\n\n  ```python\n    result = SparseTensor(input.indices, fn(input.values), input.dense_shape)\n  ```\n\n  If, however, the function is not expressible as a TensorFlow op, then use\n\n  ```python\n  result = SparseTensor(\n    input.indices, map_fn(fn, input.values), input.dense_shape)\n  ```\n\n  instead.\n\n  Args:\n    fn: The callable to be performed.  It accepts one argument, which will\n      have the same (possibly nested) structure as `elems`.  Its output\n      must have the same structure as `dtype` if one is provided, otherwise\n      it must have the same structure as `elems`.\n    elems: A tensor or (possibly nested) sequence of tensors, each of which\n      will be unpacked along their first dimension.  The nested sequence\n      of the resulting slices will be applied to `fn`.\n    dtype: (optional) The output type(s) of `fn`.  If `fn` returns a structure\n      of Tensors differing from the structure of `elems`, then `dtype` is not\n      optional and must have the same structure as the output of `fn`.\n    parallel_iterations: (optional) The number of iterations allowed to run\n      in parallel.\n    back_prop: (optional) True enables support for back propagation.\n    swap_memory: (optional) True enables GPU-CPU memory swapping.\n    infer_shape: (optional) False disables tests for consistent output shapes.\n    name: (optional) Name prefix for the returned tensors.\n\n  Returns:\n    A tensor or (possibly nested) sequence of tensors.  Each tensor packs the\n    results of applying `fn` to tensors unpacked from `elems` along the first\n    dimension, from first to last.\n\n  Raises:\n    TypeError: if `fn` is not callable or the structure of the output of\n      `fn` and `dtype` do not match, or if elems is a SparseTensor.\n    ValueError: if the lengths of the output of `fn` and `dtype` do not match.\n\n  Examples:\n    ```python\n    elems = np.array([1, 2, 3, 4, 5, 6])\n    squares = map_fn(lambda x: x * x, elems)\n    # squares == [1, 4, 9, 16, 25, 36]\n    ```\n\n    ```python\n    elems = (np.array([1, 2, 3]), np.array([-1, 1, -1]))\n    alternate = map_fn(lambda x: x[0] * x[1], elems, dtype=tf.int64)\n    # alternate == [-1, 2, -3]\n    ```\n\n    ```python\n    elems = np.array([1, 2, 3])\n    alternates = map_fn(lambda x: (x, -x), elems, dtype=(tf.int64, tf.int64))\n    # alternates[0] == [1, 2, 3]\n    # alternates[1] == [-1, -2, -3]\n    ```\n  '
    if (not callable(fn)):
        raise TypeError('fn must be callable.')
    if isinstance(elems, sparse_tensor.SparseTensor):
        raise TypeError('To perform a map on the values of a sparse tensor use either  SparseTensor(input.indices, fn(input.values), input.dense_shape) or  SparseTensor(input.indices, map_fn(fn, input.values), input.dense_shape)')
    input_is_sequence = nest.is_sequence(elems)
    input_flatten = (lambda x: (nest.flatten(x) if input_is_sequence else [x]))

    def input_pack(x):
        return (nest.pack_sequence_as(elems, x) if input_is_sequence else x[0])
    if (dtype is None):
        output_is_sequence = input_is_sequence
        output_flatten = input_flatten
        output_pack = input_pack
    else:
        output_is_sequence = nest.is_sequence(dtype)
        output_flatten = (lambda x: (nest.flatten(x) if output_is_sequence else [x]))

        def output_pack(x):
            return (nest.pack_sequence_as(dtype, x) if output_is_sequence else x[0])
    elems_flat = input_flatten(elems)
    with ops.name_scope(name, 'map', elems_flat):
        varscope = vs.get_variable_scope()
        varscope_caching_device_was_none = False
        if (varscope.caching_device is None):
            varscope.set_caching_device((lambda op: op.device))
            varscope_caching_device_was_none = True
        elems_flat = [ops.convert_to_tensor(elem, name='elem') for elem in elems_flat]
        dtype = (dtype or input_pack([elem.dtype for elem in elems_flat]))
        dtype_flat = output_flatten(dtype)
        n = array_ops.shape(elems_flat[0])[0]
        elems_ta = [tensor_array_ops.TensorArray(dtype=elem.dtype, size=n, dynamic_size=False, infer_shape=True) for elem in elems_flat]
        elems_ta = [elem_ta.unstack(elem) for (elem_ta, elem) in zip(elems_ta, elems_flat)]
        i = constant_op.constant(0)
        accs_ta = [tensor_array_ops.TensorArray(dtype=dt, size=n, dynamic_size=False, infer_shape=infer_shape) for dt in dtype_flat]

        def compute(i, tas):
            'The loop body of map_fn.\n\n      Args:\n        i: the loop counter\n        tas: the flat TensorArray accumulator list\n\n      Returns:\n        (i + 1, tas): the updated counter + updated TensorArrays\n\n      Raises:\n        TypeError: if dtype and packed_fn_values structure do not match\n        ValueType: if dtype and packed_fn_values lengths do not match\n      '
            packed_values = input_pack([elem_ta.read(i) for elem_ta in elems_ta])
            packed_fn_values = fn(packed_values)
            nest.assert_same_structure((dtype or elems), packed_fn_values)
            flat_fn_values = output_flatten(packed_fn_values)
            tas = [ta.write(i, value) for (ta, value) in zip(tas, flat_fn_values)]
            return ((i + 1), tas)
        (_, r_a) = control_flow_ops.while_loop((lambda i, _: (i < n)), compute, (i, accs_ta), parallel_iterations=parallel_iterations, back_prop=back_prop, swap_memory=swap_memory)
        results_flat = [r.stack() for r in r_a]
        n_static = elems_flat[0].get_shape().with_rank_at_least(1)[0]
        for elem in elems_flat[1:]:
            n_static.merge_with(elem.get_shape().with_rank_at_least(1)[0])
        for r in results_flat:
            r.set_shape(tensor_shape.TensorShape(n_static).concatenate(r.get_shape()[1:]))
        if varscope_caching_device_was_none:
            varscope.set_caching_device(None)
        return output_pack(results_flat)
