def choose_conv_method(in1, in2, mode='full', measure=False):
    "\n    Find the fastest convolution/correlation method.\n\n    This primarily exists to be called during the ``method='auto'`` option in\n    `convolve` and `correlate`, but can also be used when performing many\n    convolutions of the same input shapes and dtypes, determining\n    which method to use for all of them, either to avoid the overhead of the\n    'auto' option or to use accurate real-world measurements.\n\n    Parameters\n    ----------\n    in1 : array_like\n        The first argument passed into the convolution function.\n    in2 : array_like\n        The second argument passed into the convolution function.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear convolution\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    measure : bool, optional\n        If True, run and time the convolution of `in1` and `in2` with both\n        methods and return the fastest. If False (default), predict the fastest\n        method using precomputed values.\n\n    Returns\n    -------\n    method : str\n        A string indicating which convolution method is fastest, either\n        'direct' or 'fft'\n    times : dict, optional\n        A dictionary containing the times (in seconds) needed for each method.\n        This value is only returned if ``measure=True``.\n\n    See Also\n    --------\n    convolve\n    correlate\n\n    Notes\n    -----\n    For large n, ``measure=False`` is accurate and can quickly determine the\n    fastest method to perform the convolution.  However, this is not as\n    accurate for small n (when any dimension in the input or output is small).\n\n    In practice, we found that this function estimates the faster method up to\n    a multiplicative factor of 5 (i.e., the estimated method is *at most* 5\n    times slower than the fastest method). The estimation values were tuned on\n    an early 2015 MacBook Pro with 8GB RAM but we found that the prediction\n    held *fairly* accurately across different machines.\n\n    If ``measure=True``, time the convolutions. Because this function uses\n    `fftconvolve`, an error will be thrown if it does not support the inputs.\n    There are cases when `fftconvolve` supports the inputs but this function\n    returns `direct` (e.g., to protect against floating point integer\n    precision).\n\n    .. versionadded:: 0.19\n\n    Examples\n    --------\n    Estimate the fastest method for a given input:\n\n    >>> from scipy import signal\n    >>> a = np.random.randn(1000)\n    >>> b = np.random.randn(1000000)\n    >>> method = signal.choose_conv_method(a, b, mode='same')\n    >>> method\n    'fft'\n\n    This can then be applied to other arrays of the same dtype and shape:\n\n    >>> c = np.random.randn(1000)\n    >>> d = np.random.randn(1000000)\n    >>> # `method` works with correlate and convolve\n    >>> corr1 = signal.correlate(a, b, mode='same', method=method)\n    >>> corr2 = signal.correlate(c, d, mode='same', method=method)\n    >>> conv1 = signal.convolve(a, b, mode='same', method=method)\n    >>> conv2 = signal.convolve(c, d, mode='same', method=method)\n\n    "
    volume = np.asarray(in1)
    kernel = np.asarray(in2)
    if measure:
        times = {
            
        }
        for method in ['fft', 'direct']:
            times[method] = _timeit_fast((lambda : convolve(volume, kernel, mode=mode, method=method)))
        chosen_method = ('fft' if (times['fft'] < times['direct']) else 'direct')
        return (chosen_method, times)
    fftconv_unsup = ('complex256' if (sys.maxsize > (2 ** 32)) else 'complex192')
    if hasattr(np, fftconv_unsup):
        if ((volume.dtype == fftconv_unsup) or (kernel.dtype == fftconv_unsup)):
            return 'direct'
    if any([_numeric_arrays([x], kinds='ui') for x in [volume, kernel]]):
        max_value = (int(np.abs(volume).max()) * int(np.abs(kernel).max()))
        max_value *= int(min(volume.size, kernel.size))
        if (max_value > ((2 ** np.finfo('float').nmant) - 1)):
            return 'direct'
    if _numeric_arrays([volume, kernel], kinds='b'):
        return 'direct'
    if _numeric_arrays([volume, kernel]):
        if _fftconv_faster(volume, kernel, mode):
            return 'fft'
    return 'direct'