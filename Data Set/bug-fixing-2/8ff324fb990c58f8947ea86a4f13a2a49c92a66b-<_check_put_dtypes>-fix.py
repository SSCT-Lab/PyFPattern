

def _check_put_dtypes(self, vals, indices=None):
    'Validate and convert `vals` to a list of `Tensor`s.\n\n    The `vals` argument can be a Tensor, a list or tuple of tensors, or a\n    dictionary with tensor values.\n\n    If `vals` is a list, then the appropriate indices associated with the\n    values must be provided.\n\n    If it is a dictionary, the staging area must have been constructed with a\n    `names` attribute and the dictionary keys must match the staging area names.\n    `indices` will be inferred from the dictionary keys.\n    If the staging area was constructed with a `names` attribute, `vals` must\n    be a dictionary.\n\n    Checks that the dtype and shape of each value matches that\n    of the staging area.\n\n    Args:\n      vals: A tensor, a list or tuple of tensors, or a dictionary..\n\n    Returns:\n      A (tensors, indices) tuple where `tensors` is a list of `Tensor` objects\n      and `indices` is a list of indices associed with the tensors.\n\n    Raises:\n      ValueError: If `vals` or `indices` is invalid.\n    '
    if isinstance(vals, dict):
        if (not self._names):
            raise ValueError('Staging areas must have names to enqueue a dictionary')
        if (not set(vals.keys()).issubset(self._names)):
            raise ValueError(('Keys in dictionary to put do not match names of staging area. Dictionary: (%s), Queue: (%s)' % (sorted(vals.keys()), sorted(self._names))))
        (vals, indices, n) = zip(*[(vals[k], i, k) for (i, k) in enumerate(self._names) if (k in vals)])
    else:
        if self._names:
            raise ValueError('You must enqueue a dictionary in a staging area with names')
        if (indices is None):
            raise ValueError('Indices must be supplied when inserting a list of tensors')
        if (len(indices) != len(vals)):
            raise ValueError("Number of indices '%s' doesn't match number of values '%s'")
        if (not isinstance(vals, (list, tuple))):
            vals = [vals]
            indices = [0]
    if (not (len(vals) <= len(self._dtypes))):
        raise ValueError(("Unexpected number of inputs '%s' vs '%s'" % (len(vals), len(self._dtypes))))
    tensors = []
    for (val, i) in zip(vals, indices):
        (dtype, shape) = (self._dtypes[i], self._shapes[i])
        if (not (val.dtype == dtype)):
            raise ValueError(("Datatypes do not match. '%s' != '%s'" % (str(val.dtype), str(dtype))))
        val.get_shape().assert_is_compatible_with(shape)
        tensors.append(ops.convert_to_tensor(val, dtype=dtype, name=('component_%d' % i)))
    return (tensors, indices)
