

def _ragged_getitem(rt_input, key_list):
    'Helper for indexing and slicing ragged tensors with __getitem__().\n\n  Extracts the specified piece of the `rt_input`.  See\n  `RaggedTensor.__getitem__` for examples and restrictions.\n\n  Args:\n    rt_input: The `RaggedTensor` from which a piece should be returned.\n    key_list: The list of keys specifying which piece to return. Each key\n      corresponds with a separate dimension.\n\n  Returns:\n    The indicated piece of rt_input.\n\n  Raises:\n    ValueError: If `key_list` is not supported.\n    TypeError: If any keys in `key_list` have an unsupported type.\n  '
    if (not key_list):
        return rt_input
    row_key = key_list[0]
    inner_keys = key_list[1:]
    if (row_key is Ellipsis):
        expanded_key_list = _expand_ellipsis(key_list, rt_input.shape.ndims)
        return _ragged_getitem(rt_input, expanded_key_list)
    if (row_key is array_ops.newaxis):
        inner_rt = _ragged_getitem(rt_input, inner_keys)
        nsplits = array_ops.shape(inner_rt.row_splits, out_type=dtypes.int64)[0]
        return ragged_tensor.RaggedTensor.from_row_splits(inner_rt, array_ops.stack([0, (nsplits - 1)]))
    if isinstance(row_key, slice):
        sliced_rt_input = _slice_ragged_row_dimension(rt_input, row_key)
        return _ragged_getitem_inner_dimensions(sliced_rt_input, inner_keys)
    else:
        starts = rt_input.row_splits[:(- 1)]
        limits = rt_input.row_splits[1:]
        if context.executing_eagerly():
            try:
                if (row_key >= len(starts)):
                    raise IndexError('Row key {} out of bounds'.format(row_key))
            except TypeError:
                pass
        row = rt_input.values[starts[row_key]:limits[row_key]]
        return row.__getitem__(inner_keys)
