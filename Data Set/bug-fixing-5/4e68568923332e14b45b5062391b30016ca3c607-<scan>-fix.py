@tf_export('scan')
def scan(fn, elems, initializer=None, parallel_iterations=10, back_prop=True, swap_memory=False, infer_shape=True, name=None):
    'scan on the list of tensors unpacked from `elems` on dimension 0.\n\n  The simplest version of `scan` repeatedly applies the callable `fn` to a\n  sequence of elements from first to last. The elements are made of the tensors\n  unpacked from `elems` on dimension 0. The callable fn takes two tensors as\n  arguments. The first argument is the accumulated value computed from the\n  preceding invocation of fn. If `initializer` is None, `elems` must contain\n  at least one element, and its first element is used as the initializer.\n\n  Suppose that `elems` is unpacked into `values`, a list of tensors. The shape\n  of the result tensor is `[len(values)] + fn(initializer, values[0]).shape`.\n\n  This method also allows multi-arity `elems` and accumulator.  If `elems`\n  is a (possibly nested) list or tuple of tensors, then each of these tensors\n  must have a matching first (unpack) dimension.  The second argument of\n  `fn` must match the structure of `elems`.\n\n  If no `initializer` is provided, the output structure and dtypes of `fn`\n  are assumed to be the same as its input; and in this case, the first\n  argument of `fn` must match the structure of `elems`.\n\n  If an `initializer` is provided, then the output of `fn` must have the same\n  structure as `initializer`; and the first argument of `fn` must match\n  this structure.\n\n  For example, if `elems` is `(t1, [t2, t3])` and `initializer` is\n  `[i1, i2]` then an appropriate signature for `fn` in `python2` is:\n  `fn = lambda (acc_p1, acc_p2), (t1, [t2, t3]):` and `fn` must return a list,\n  `[acc_n1, acc_n2]`.  An alternative correct signature for `fn`, and the\n   one that works in `python3`, is:\n  `fn = lambda a, t:`, where `a` and `t` correspond to the input tuples.\n\n  Args:\n    fn: The callable to be performed.  It accepts two arguments.  The first\n      will have the same structure as `initializer` if one is provided,\n      otherwise it will have the same structure as `elems`.  The second\n      will have the same (possibly nested) structure as `elems`.  Its output\n      must have the same structure as `initializer` if one is provided,\n      otherwise it must have the same structure as `elems`.\n    elems: A tensor or (possibly nested) sequence of tensors, each of which\n      will be unpacked along their first dimension.  The nested sequence\n      of the resulting slices will be the first argument to `fn`.\n    initializer: (optional) A tensor or (possibly nested) sequence of tensors,\n      initial value for the accumulator, and the expected output type of `fn`.\n    parallel_iterations: (optional) The number of iterations allowed to run\n      in parallel.\n    back_prop: (optional) True enables support for back propagation.\n    swap_memory: (optional) True enables GPU-CPU memory swapping.\n    infer_shape: (optional) False disables tests for consistent output shapes.\n    name: (optional) Name prefix for the returned tensors.\n\n  Returns:\n    A tensor or (possibly nested) sequence of tensors.  Each tensor packs the\n    results of applying `fn` to tensors unpacked from `elems` along the first\n    dimension, and the previous accumulator value(s), from first to last.\n\n  Raises:\n    TypeError: if `fn` is not callable or the structure of the output of\n      `fn` and `initializer` do not match.\n    ValueError: if the lengths of the output of `fn` and `initializer`\n      do not match.\n\n  Examples:\n    ```python\n    elems = np.array([1, 2, 3, 4, 5, 6])\n    sum = scan(lambda a, x: a + x, elems)\n    # sum == [1, 3, 6, 10, 15, 21]\n    ```\n\n    ```python\n    elems = np.array([1, 2, 3, 4, 5, 6])\n    initializer = np.array(0)\n    sum_one = scan(\n        lambda a, x: x[0] - x[1] + a, (elems + 1, elems), initializer)\n    # sum_one == [1, 2, 3, 4, 5, 6]\n    ```\n\n    ```python\n    elems = np.array([1, 0, 0, 0, 0, 0])\n    initializer = (np.array(0), np.array(1))\n    fibonaccis = scan(lambda a, _: (a[1], a[0] + a[1]), elems, initializer)\n    # fibonaccis == ([1, 1, 2, 3, 5, 8], [1, 2, 3, 5, 8, 13])\n    ```\n  '
    if (not callable(fn)):
        raise TypeError('fn must be callable.')
    input_is_sequence = nest.is_sequence(elems)
    input_flatten = (lambda x: (nest.flatten(x) if input_is_sequence else [x]))

    def input_pack(x):
        return (nest.pack_sequence_as(elems, x) if input_is_sequence else x[0])
    if (initializer is None):
        output_is_sequence = input_is_sequence
        output_flatten = input_flatten
        output_pack = input_pack
    else:
        output_is_sequence = nest.is_sequence(initializer)
        output_flatten = (lambda x: (nest.flatten(x) if output_is_sequence else [x]))

        def output_pack(x):
            return (nest.pack_sequence_as(initializer, x) if output_is_sequence else x[0])
    elems_flat = input_flatten(elems)
    in_graph_mode = context.in_graph_mode()
    with ops.name_scope(name, 'scan', elems_flat):
        if in_graph_mode:
            varscope = vs.get_variable_scope()
            varscope_caching_device_was_none = False
            if (varscope.caching_device is None):
                varscope.set_caching_device((lambda op: op.device))
                varscope_caching_device_was_none = True
        elems_flat = [ops.convert_to_tensor(elem, name='elem') for elem in elems_flat]
        n = array_ops.shape(elems_flat[0])[0]
        elems_ta = [tensor_array_ops.TensorArray(dtype=elem.dtype, size=n, dynamic_size=False, infer_shape=True) for elem in elems_flat]
        elems_ta = [elem_ta.unstack(elem) for (elem_ta, elem) in zip(elems_ta, elems_flat)]
        if (initializer is None):
            a_flat = [elem.read(0) for elem in elems_ta]
            i = constant_op.constant(1)
        else:
            initializer_flat = output_flatten(initializer)
            a_flat = [ops.convert_to_tensor(init) for init in initializer_flat]
            i = constant_op.constant(0)
        accs_ta = [tensor_array_ops.TensorArray(dtype=init.dtype, size=n, element_shape=(init.shape if infer_shape else None), dynamic_size=False, infer_shape=infer_shape) for init in a_flat]
        if (initializer is None):
            accs_ta = [acc_ta.write(0, a) for (acc_ta, a) in zip(accs_ta, a_flat)]

        def compute(i, a_flat, tas):
            'The loop body of scan.\n\n      Args:\n        i: the loop counter.\n        a_flat: the accumulator value(s), flattened.\n        tas: the output accumulator TensorArray(s), flattened.\n\n      Returns:\n        [i + 1, a_flat, tas]: the updated counter + new accumulator values +\n          updated TensorArrays\n\n      Raises:\n        TypeError: if initializer and fn() output structure do not match\n        ValueType: if initializer and fn() output lengths do not match\n      '
            packed_elems = input_pack([elem_ta.read(i) for elem_ta in elems_ta])
            packed_a = output_pack(a_flat)
            a_out = fn(packed_a, packed_elems)
            nest.assert_same_structure((elems if (initializer is None) else initializer), a_out)
            flat_a_out = output_flatten(a_out)
            tas = [ta.write(i, value) for (ta, value) in zip(tas, flat_a_out)]
            return ((i + 1), flat_a_out, tas)
        (_, _, r_a) = control_flow_ops.while_loop((lambda i, _1, _2: (i < n)), compute, (i, a_flat, accs_ta), parallel_iterations=parallel_iterations, back_prop=back_prop, swap_memory=swap_memory)
        results_flat = [r.stack() for r in r_a]
        n_static = elems_flat[0].get_shape().with_rank_at_least(1)[0]
        for elem in elems_flat[1:]:
            n_static.merge_with(elem.get_shape().with_rank_at_least(1)[0])
        for r in results_flat:
            r.set_shape(tensor_shape.TensorShape(n_static).concatenate(r.get_shape()[1:]))
        if (in_graph_mode and varscope_caching_device_was_none):
            varscope.set_caching_device(None)
        return output_pack(results_flat)