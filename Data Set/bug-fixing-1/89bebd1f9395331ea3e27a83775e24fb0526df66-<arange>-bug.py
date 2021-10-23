

def arange(start, stop=None, step=1.0, repeat=1, infer_range=False, name=None, dtype=None):
    'Returns evenly spaced values within a given interval.\n\n    Parameters\n    ----------\n    start : number\n        Start of interval. The interval includes this value. The default start value is 0.\n    stop : number, optional\n        End of interval. The interval does not include this value.\n    step : number, optional\n        Spacing between values.\n    repeat : int, optional\n        "The repeating time of all elements.\n        E.g repeat=3, the element a will be repeated three times --> a, a, a.\n    infer_range : boolean, optional\n        When set to True, infer the stop position from the start, step,\n        repeat, and output tensor size.\n    dtype : str or numpy.dtype, optional\n        The value type of the inner value, default to ``np.float32``.\n\n    Returns\n    -------\n    out : Symbol\n        The created Symbol\n    '
    if (dtype is None):
        dtype = _numpy.float32
    return _internal._arange(start=start, stop=stop, step=step, repeat=repeat, infer_range=infer_range, name=name, dtype=dtype)
