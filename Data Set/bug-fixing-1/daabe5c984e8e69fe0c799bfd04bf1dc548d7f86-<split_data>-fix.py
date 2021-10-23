

def split_data(data, num_slice, batch_axis=0, even_split=True):
    'Splits an NDArray into `num_slice` slices along `batch_axis`.\n    Usually used for data parallelism where each slices is sent\n    to one device (i.e. GPU).\n\n    Parameters\n    ----------\n    data : NDArray\n        A batch of data.\n    num_slice : int\n        Number of desired slices.\n    batch_axis : int, default 0\n        The axis along which to slice.\n    even_split : bool, default True\n        Whether to force all slices to have the same number of elements.\n        If `True`, an error will be raised when `num_slice` does not evenly\n        divide `data.shape[batch_axis]`.\n\n    Returns\n    -------\n    list of NDArray\n        Return value is a list even if `num_slice` is 1.\n    '
    size = data.shape[batch_axis]
    if (even_split and ((size % num_slice) != 0)):
        raise ValueError(("data with shape %s cannot be evenly split into %d slices along axis %d. Use a batch size that's multiple of %d or set even_split=False to allow uneven partitioning of data." % (str(data.shape), num_slice, batch_axis, num_slice)))
    step = (size // num_slice)
    if ((not even_split) and (size < num_slice)):
        step = 1
        num_slice = size
    if (batch_axis == 0):
        slices = [(data[(i * step):((i + 1) * step)] if (i < (num_slice - 1)) else data[(i * step):size]) for i in range(num_slice)]
    elif even_split:
        slices = ndarray.split(data, num_outputs=num_slice, axis=batch_axis)
    else:
        slices = [(ndarray.slice_axis(data, batch_axis, (i * step), ((i + 1) * step)) if (i < (num_slice - 1)) else ndarray.slice_axis(data, batch_axis, (i * step), size)) for i in range(num_slice)]
    return slices
