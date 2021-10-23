def _SliceHelper(tensor, slice_spec, var=None):
    'Overload for Tensor.__getitem__.\n\n  This operation extracts the specified region from the tensor.\n  The notation is similar to NumPy with the restriction that\n  currently only support basic indexing. That means that\n  using a tensor as input is not currently allowed\n\n  Some useful examples:\n\n  ```python\n  # strip leading and trailing 2 elements\n  foo = tf.constant([1,2,3,4,5,6])\n  print(foo[2:-2].eval()) # => [3,4]\n\n  # skip every row and reverse every column\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[::2,::-1].eval()) # => [[3,2,1], [9,8,7]]\n\n  # Insert another dimension\n  foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])\n  print(foo[tf.newaxis, :, :].eval()) # => [[[1,2,3], [4,5,6], [7,8,9]]]\n  print(foo[:, tf.newaxis, :].eval()) # => [[[1,2,3]], [[4,5,6]], [[7,8,9]]]\n  print(foo[:, :, tf.newaxis].eval()) # => [[[1],[2],[3]], [[4],[5],[6]], [[7],[8],[9]]]\n\n  # Ellipses (3 equivalent operations)\n  print(foo[tf.newaxis, :, :].eval()) # => [[[3,2,1], [9,8,7]]]\n  print(foo[tf.newaxis, ...].eval()) # => [[[3,2,1], [9,8,7]]]\n  print(foo[tf.newaxis].eval()) # => [[[3,2,1], [9,8,7]]]\n  ```\n\n  Notes:\n    - `tf.newaxis` is `None` as in NumPy.\n    - An implicit ellipsis is placed at the end of the `slice_spec`\n    - NumPy advanced indexing is currently not supported.\n\n  Args:\n    tensor: An ops.Tensor object.\n    slice_spec: The arguments to Tensor.__getitem__.\n    var: In the case of variable slice assignment, the Variable\n      object to slice (i.e. tensor is the read-only view of this\n      variable).\n\n  Returns:\n    The appropriate slice of "tensor", based on "slice_spec".\n\n  Raises:\n    ValueError: If a slice range is negative size.\n    TypeError: If the slice indices aren\'t int, slice, or Ellipsis.\n  '
    if (not isinstance(slice_spec, (list, tuple))):
        slice_spec = [slice_spec]
    (begin, end, strides) = ([], [], [])
    index = 0
    (new_axis_mask, shrink_axis_mask) = (0, 0)
    (begin_mask, end_mask) = (0, 0)
    ellipsis_mask = 0
    for s in slice_spec:
        if isinstance(s, _baseslice):
            strides.append((s.step if (s.step is not None) else 1))
            if ((s.start is not None) and (s.start is not sys.maxsize)):
                begin.append(s.start)
            else:
                begin.append(0)
                begin_mask |= (1 << index)
            if ((s.stop is not None) and (s.stop != sys.maxsize)):
                end.append(s.stop)
            else:
                end.append(0)
                end_mask |= (1 << index)
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
            begin.append(s)
            end.append((s + 1))
            if isinstance(s, ops.Tensor):
                strides.append(constant(1, s.dtype))
            else:
                strides.append(np.ones_like(s).dtype.type(1))
            shrink_axis_mask |= (1 << index)
        index += 1
    with ops.name_scope(None, 'strided_slice', ((([tensor] + begin) + end) + strides)) as name:
        if begin:
            (packed_begin, packed_end, packed_strides) = (stack(begin), stack(end), stack(strides))
        else:
            var_empty = constant([], dtype=dtypes.int32)
            packed_begin = packed_end = packed_strides = var_empty
        return strided_slice(tensor, packed_begin, packed_end, packed_strides, begin_mask=begin_mask, end_mask=end_mask, shrink_axis_mask=shrink_axis_mask, new_axis_mask=new_axis_mask, ellipsis_mask=ellipsis_mask, var=var, name=name)