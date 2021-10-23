def _slice_helper(tensor, slice_spec, var=None):
    'Overload for Tensor.__getitem__.\n\n  This operation extracts the specified region from the tensor.\n  The notation is similar to NumPy with the restriction that\n  currently only support basic indexing. That means that\n  using a non-scalar tensor as input is not currently allowed.\n\n  Some useful examples:\n\n  ```python\n  # strip leading and trailing 2 elements\n  foo = tf.constant([1,2,3,4,5,6])\n  print(foo[2:-2].eval())  # => [3,4]\n\n  # skip every row and reverse every column\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[::2,::-1].eval())  # => [[3,2,1], [9,8,7]]\n\n  # Use scalar tensors as indices on both dimensions\n  print(foo[tf.constant(0), tf.constant(2)].eval())  # => 3\n\n  # Insert another dimension\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[tf.newaxis, :, :].eval()) # => [[[1,2,3], [4,5,6], [7,8,9]]]\n  print(foo[:, tf.newaxis, :].eval()) # => [[[1,2,3]], [[4,5,6]], [[7,8,9]]]\n  print(foo[:, :, tf.newaxis].eval()) # => [[[1],[2],[3]], [[4],[5],[6]],\n  [[7],[8],[9]]]\n\n  # Ellipses (3 equivalent operations)\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[tf.newaxis, :, :].eval())  # => [[[1,2,3], [4,5,6], [7,8,9]]]\n  print(foo[tf.newaxis, ...].eval())  # => [[[1,2,3], [4,5,6], [7,8,9]]]\n  print(foo[tf.newaxis].eval())  # => [[[1,2,3], [4,5,6], [7,8,9]]]\n\n  # masks\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[foo > 2].eval())  # => [3, 4, 5, 6, 7, 8, 9]\n  ```\n\n  Notes:\n    - `tf.newaxis` is `None` as in NumPy.\n    - An implicit ellipsis is placed at the end of the `slice_spec`\n    - NumPy advanced indexing is currently not supported.\n\n  Args:\n    tensor: An ops.Tensor object.\n    slice_spec: The arguments to Tensor.__getitem__.\n    var: In the case of variable slice assignment, the Variable\n      object to slice (i.e. tensor is the read-only view of this\n      variable).\n\n  Returns:\n    The appropriate slice of "tensor", based on "slice_spec".\n\n  Raises:\n    ValueError: If a slice range is negative size.\n    TypeError: If the slice indices aren\'t int, slice, ellipsis,\n      tf.newaxis or scalar int32/int64 tensors.\n  '
    if (isinstance(slice_spec, bool) or (isinstance(slice_spec, ops.Tensor) and (slice_spec.dtype == dtypes.bool)) or (isinstance(slice_spec, np.ndarray) and (slice_spec.dtype == bool))):
        return boolean_mask(tensor=tensor, mask=slice_spec)
    if (not isinstance(slice_spec, (list, tuple))):
        slice_spec = [slice_spec]
    (begin, end, strides) = ([], [], [])
    index = 0
    (new_axis_mask, shrink_axis_mask) = (0, 0)
    (begin_mask, end_mask) = (0, 0)
    ellipsis_mask = 0
    for s in slice_spec:
        if isinstance(s, _BaseSlice):
            if ((s.start is not None) and (s.start is not sys.maxsize)):
                _check_index(s.start)
                begin.append(s.start)
            else:
                begin.append(0)
                begin_mask |= (1 << index)
            if ((s.stop is not None) and (s.stop != sys.maxsize)):
                _check_index(s.stop)
                end.append(s.stop)
            else:
                end.append(0)
                end_mask |= (1 << index)
            if (s.step is not None):
                _check_index(s.step)
                strides.append(s.step)
            else:
                strides.append(1)
        elif (s is Ellipsis):
            begin.append(0)
            end.append(0)
            strides.append(1)
            ellipsis_mask |= (1 << index)
        elif (s is newaxis):
            begin.append(0)
            end.append(0)
            strides.append(1)
            new_axis_mask |= (1 << index)
        else:
            _check_index(s)
            begin.append(s)
            end.append((s + 1))
            strides.append(1)
            shrink_axis_mask |= (1 << index)
        index += 1
    with ops.name_scope(None, 'strided_slice', ((([tensor] + begin) + end) + strides)) as name:
        if begin:
            (packed_begin, packed_end, packed_strides) = (stack(begin), stack(end), stack(strides))
            if ((packed_begin.dtype == dtypes.int64) or (packed_end.dtype == dtypes.int64) or (packed_strides.dtype == dtypes.int64)):
                if (packed_begin.dtype != dtypes.int64):
                    packed_begin = gen_math_ops.cast(packed_begin, dtypes.int64)
                if (packed_end.dtype != dtypes.int64):
                    packed_end = gen_math_ops.cast(packed_end, dtypes.int64)
                if (packed_strides.dtype != dtypes.int64):
                    packed_strides = gen_math_ops.cast(packed_strides, dtypes.int64)
        else:
            var_empty = constant([], dtype=dtypes.int32)
            packed_begin = packed_end = packed_strides = var_empty
        return strided_slice(tensor, packed_begin, packed_end, packed_strides, begin_mask=begin_mask, end_mask=end_mask, shrink_axis_mask=shrink_axis_mask, new_axis_mask=new_axis_mask, ellipsis_mask=ellipsis_mask, var=var, name=name)