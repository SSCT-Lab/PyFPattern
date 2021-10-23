

def streaming_concat(values, axis=0, max_size=None, metrics_collections=None, updates_collections=None, name=None):
    'Concatenate values along an axis across batches.\n\n  The function `streaming_concat` creates two local variables, `array` and\n  `size`, that are used to store concatenated values. Internally, `array` is\n  used as storage for a dynamic array (if `maxsize` is `None`), which ensures\n  that updates can be run in amortized constant time.\n\n  For estimation of the metric over a stream of data, the function creates an\n  `update_op` operation that appends the values of a tensor and returns the\n  `value` of the concatenated tensors.\n\n  This op allows for evaluating metrics that cannot be updated incrementally\n  using the same framework as other streaming metrics.\n\n  Args:\n    values: `Tensor` to concatenate. Rank and the shape along all axes other\n      than the axis to concatenate along must be statically known.\n    axis: optional integer axis to concatenate along.\n    max_size: optional integer maximum size of `value` along the given axis.\n      Once the maximum size is reached, further updates are no-ops. By default,\n      there is no maximum size: the array is resized as necessary.\n    metrics_collections: An optional list of collections that `value`\n      should be added to.\n    updates_collections: An optional list of collections `update_op` should be\n      added to.\n    name: An optional variable_scope name.\n\n  Returns:\n    value: A `Tensor` representing the concatenated values.\n    update_op: An operation that concatenates the next values.\n\n  Raises:\n    ValueError: if `values` does not have a statically known rank, `axis` is\n      not in the valid range or the size of `values` is not statically known\n      along any axis other than `axis`.\n  '
    with variable_scope.variable_scope(name, 'streaming_concat', (values,)):
        values_shape = values.get_shape()
        if (values_shape.dims is None):
            raise ValueError('`values` must have known statically known rank')
        ndim = len(values_shape)
        if (axis < 0):
            axis += ndim
        if (not (0 <= axis < ndim)):
            raise ValueError(('axis = %r not in [0, %r)' % (axis, ndim)))
        fixed_shape = [dim.value for (n, dim) in enumerate(values_shape) if (n != axis)]
        if any(((value is None) for value in fixed_shape)):
            raise ValueError('all dimensions of `values` other than the dimension to concatenate along must have statically known size')
        init_size = (0 if (max_size is None) else max_size)
        init_shape = ([init_size] + fixed_shape)
        array = _create_local('array', shape=init_shape, validate_shape=False, dtype=values.dtype)
        size = _create_local('size', shape=[], dtype=dtypes.int32)
        perm = [(0 if (n == axis) else ((n + 1) if (n < axis) else n)) for n in range(ndim)]
        valid_array = array[:size]
        valid_array.set_shape(([None] + fixed_shape))
        value = array_ops.transpose(valid_array, perm, name='concat')
        values_size = array_ops.shape(values)[axis]
        if (max_size is None):
            batch_size = values_size
        else:
            batch_size = math_ops.minimum(values_size, (max_size - size))
        perm = ([axis] + [n for n in range(ndim) if (n != axis)])
        batch_values = array_ops.transpose(values, perm)[:batch_size]

        def reallocate():
            next_size = _next_array_size(new_size)
            next_shape = array_ops.stack(([next_size] + fixed_shape))
            new_value = array_ops.zeros(next_shape, dtype=values.dtype)
            old_value = array.value()
            assign_op = state_ops.assign(array, new_value, validate_shape=False)
            with ops.control_dependencies([assign_op]):
                copy_op = array[:size].assign(old_value[:size])
            with ops.control_dependencies([copy_op]):
                return control_flow_ops.no_op()
        new_size = (size + batch_size)
        array_size = array_ops.shape_internal(array, optimize=False)[0]
        maybe_reallocate_op = control_flow_ops.cond((new_size > array_size), reallocate, control_flow_ops.no_op)
        with ops.control_dependencies([maybe_reallocate_op]):
            append_values_op = array[size:new_size].assign(batch_values)
        with ops.control_dependencies([append_values_op]):
            update_op = size.assign(new_size)
        if metrics_collections:
            ops.add_to_collections(metrics_collections, value)
        if updates_collections:
            ops.add_to_collections(updates_collections, update_op)
        return (value, update_op)
