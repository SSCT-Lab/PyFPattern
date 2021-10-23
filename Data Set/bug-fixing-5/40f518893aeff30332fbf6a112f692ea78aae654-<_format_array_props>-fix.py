def _format_array_props(arrays):
    assert isinstance(arrays, (list, tuple))
    return ', '.join([(None if (arr is None) else '{}:{}'.format(arr.shape, arr.dtype.name)) for arr in arrays])