@set_module('mxnet.symbol.numpy')
def arange(start, stop=None, step=1, dtype=None, ctx=None):
    'Return evenly spaced values within a given interval.\n\n    Values are generated within the half-open interval ``[start, stop)``\n    (in other words, the interval including `start` but excluding `stop`).\n    For integer arguments the function is equivalent to the Python built-in\n    `range` function, but returns an ndarray rather than a list.\n\n    Parameters\n    ----------\n    start : number, optional\n        Start of interval. The interval includes this value.  The default\n        start value is 0.\n    stop : number\n        End of interval. The interval does not include this value, except\n        in some cases where `step` is not an integer and floating point\n        round-off affects the length of `out`.\n    step : number, optional\n        Spacing between values. For any output `out`, this is the distance\n        between two adjacent values, ``out[i+1] - out[i]``.  The default\n        step size is 1.  If `step` is specified as a position argument,\n        `start` must also be given.\n    dtype : dtype\n        The type of the output array. The default is `float32`.\n\n    Returns\n    -------\n    arange : ndarray\n        Array of evenly spaced values.\n\n        For floating point arguments, the length of the result is\n        ``ceil((stop - start)/step)``.  Because of floating point overflow,\n        this rule may result in the last element of `out` being greater\n        than `stop`.\n    '
    if (dtype is None):
        dtype = 'float32'
    if (ctx is None):
        ctx = current_context()
    if (stop is None):
        stop = start
        start = 0
    if (step is None):
        step = 1
    if ((start is None) and (stop is None)):
        raise ValueError('start and stop cannot be both None')
    if (step == 0):
        raise ZeroDivisionError('step cannot be 0')
    return _npi.arange(start=start, stop=stop, step=step, dtype=dtype, ctx=ctx)