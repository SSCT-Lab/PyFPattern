

def generate_array(initializer, shape, xp, dtype=None, device=None):
    'Return initialized array.\n\n    The algorithms used to make the new values depend on the\n    concrete derived classes. If the initializer has the ``dtype`` attribute,\n    it is used to construct the array. Otherwise, ``chainer.config.dtype`` is\n    used instead. See :ref:`configuration` for the dtype config.\n\n    Args:\n        initializer: A callable object that takes :ref:`ndarray` and edits its\n            value.\n        shape (tuple): Shape of a return array.\n        xp (module): :mod:`cupy`, :mod:`numpy`, or :mod:`chainerx`.\n        dtype: Dtype specifier. If omitted, ``initializer.dtype`` is used.\n        device: Target device specifier. If omitted, the current device is\n             used for :mod:`cupy`, and the default device is used for\n             :mod:`chainerx`.\n\n    Returns:\n        :ref:`ndarray`: An initialized array.\n\n    '
    dtype_attr = getattr(initializer, 'dtype', None)
    if ((dtype is not None) and (dtype_attr is not None) and (numpy.dtype(dtype) != numpy.dtype(dtype_attr))):
        raise ValueError('dtype mismatch: {} != {}'.format(dtype, dtype_attr))
    if (dtype is None):
        dtype = dtype_attr
    dtype = chainer.get_dtype(dtype)
    if (device is None):
        backend_device = backend._guess_device_from_array_module(xp)
    else:
        backend_device = chainer.get_device(device)
        if (xp != backend_device.xp):
            raise ValueError('xp and device arguments are inconsistent.')
    if (xp is chainerx):
        chx_device = backend_device.device
        array = chainerx.empty(shape, dtype=dtype, device=chx_device)
        fallback_device = backend_device.fallback_device
        with chainer.using_device(fallback_device):
            initializer(fallback_device.send(array))
        return array
    with chainer.using_device(backend_device):
        array = xp.empty(shape, dtype=dtype)
        initializer(array)
    return array
