def resample_poly(x, up, down, axis=0, window=('kaiser', 5.0), padtype='constant', cval=None):
    "\n    Resample `x` along the given axis using polyphase filtering.\n\n    The signal `x` is upsampled by the factor `up`, a zero-phase low-pass\n    FIR filter is applied, and then it is downsampled by the factor `down`.\n    The resulting sample rate is ``up / down`` times the original sample\n    rate. By default, values beyond the boundary of the signal are assumed\n    to be zero during the filtering step.\n\n    Parameters\n    ----------\n    x : array_like\n        The data to be resampled.\n    up : int\n        The upsampling factor.\n    down : int\n        The downsampling factor.\n    axis : int, optional\n        The axis of `x` that is resampled. Default is 0.\n    window : string, tuple, or array_like, optional\n        Desired window to use to design the low-pass filter, or the FIR filter\n        coefficients to employ. See below for details.\n    padtype : string, optional\n        `constant`, `line`, `mean`, `median`, `maximum`, `minimum` or any of\n        the other signal extension modes supported by `scipy.signal.upfirdn`.\n        Changes assumptions on values beyond the boundary. If `constant`,\n        assumed to be `cval` (default zero). If `line` assumed to continue a\n        linear trend defined by the first and last points. `mean`, `median`,\n        `maximum` and `minimum` work as in `np.pad` and assume that the values\n        beyond the boundary are the mean, median, maximum or minimum\n        respectively of the array along the axis.\n\n        .. versionadded:: 1.4.0\n    cval : float, optional\n        Value to use if `padtype='constant'`. Default is zero.\n\n        .. versionadded:: 1.4.0\n\n    Returns\n    -------\n    resampled_x : array\n        The resampled array.\n\n    See Also\n    --------\n    decimate : Downsample the signal after applying an FIR or IIR filter.\n    resample : Resample up or down using the FFT method.\n\n    Notes\n    -----\n    This polyphase method will likely be faster than the Fourier method\n    in `scipy.signal.resample` when the number of samples is large and\n    prime, or when the number of samples is large and `up` and `down`\n    share a large greatest common denominator. The length of the FIR\n    filter used will depend on ``max(up, down) // gcd(up, down)``, and\n    the number of operations during polyphase filtering will depend on\n    the filter length and `down` (see `scipy.signal.upfirdn` for details).\n\n    The argument `window` specifies the FIR low-pass filter design.\n\n    If `window` is an array_like it is assumed to be the FIR filter\n    coefficients. Note that the FIR filter is applied after the upsampling\n    step, so it should be designed to operate on a signal at a sampling\n    frequency higher than the original by a factor of `up//gcd(up, down)`.\n    This function's output will be centered with respect to this array, so it\n    is best to pass a symmetric filter with an odd number of samples if, as\n    is usually the case, a zero-phase filter is desired.\n\n    For any other type of `window`, the functions `scipy.signal.get_window`\n    and `scipy.signal.firwin` are called to generate the appropriate filter\n    coefficients.\n\n    The first sample of the returned vector is the same as the first\n    sample of the input vector. The spacing between samples is changed\n    from ``dx`` to ``dx * down / float(up)``.\n\n    Examples\n    --------\n    By default, the end of the resampled data rises to meet the first\n    sample of the next cycle for the FFT method, and gets closer to zero\n    for the polyphase method:\n\n    >>> from scipy import signal\n\n    >>> x = np.linspace(0, 10, 20, endpoint=False)\n    >>> y = np.cos(-x**2/6.0)\n    >>> f_fft = signal.resample(y, 100)\n    >>> f_poly = signal.resample_poly(y, 100, 20)\n    >>> xnew = np.linspace(0, 10, 100, endpoint=False)\n\n    >>> import matplotlib.pyplot as plt\n    >>> plt.plot(xnew, f_fft, 'b.-', xnew, f_poly, 'r.-')\n    >>> plt.plot(x, y, 'ko-')\n    >>> plt.plot(10, y[0], 'bo', 10, 0., 'ro')  # boundaries\n    >>> plt.legend(['resample', 'resamp_poly', 'data'], loc='best')\n    >>> plt.show()\n\n    This default behaviour can be changed by using the padtype option:\n\n    >>> import numpy as np\n    >>> from scipy import signal\n\n    >>> N = 5\n    >>> x = np.linspace(0, 1, N, endpoint=False)\n    >>> y = 2 + x**2 - 1.7*np.sin(x) + .2*np.cos(11*x)\n    >>> y2 = 1 + x**3 + 0.1*np.sin(x) + .1*np.cos(11*x)\n    >>> Y = np.stack([y, y2], axis=-1)\n    >>> up = 4\n    >>> xr = np.linspace(0, 1, N*up, endpoint=False)\n\n    >>> y2 = signal.resample_poly(Y, up, 1, padtype='constant')\n    >>> y3 = signal.resample_poly(Y, up, 1, padtype='mean')\n    >>> y4 = signal.resample_poly(Y, up, 1, padtype='line')\n\n    >>> import matplotlib.pyplot as plt\n    >>> for i in [0,1]:\n    ...     plt.figure()\n    ...     plt.plot(xr, y4[:,i], 'g.', label='line')\n    ...     plt.plot(xr, y3[:,i], 'y.', label='mean')\n    ...     plt.plot(xr, y2[:,i], 'r.', label='constant')\n    ...     plt.plot(x, Y[:,i], 'k-')\n    ...     plt.legend()\n    >>> plt.show()\n\n    "
    x = np.asarray(x)
    if (up != int(up)):
        raise ValueError('up must be an integer')
    if (down != int(down)):
        raise ValueError('down must be an integer')
    up = int(up)
    down = int(down)
    if ((up < 1) or (down < 1)):
        raise ValueError('up and down must be >= 1')
    if ((cval is not None) and (padtype != 'constant')):
        raise ValueError('cval has no effect when padtype is ', padtype)
    g_ = gcd(up, down)
    up //= g_
    down //= g_
    if (up == down == 1):
        return x.copy()
    n_in = x.shape[axis]
    n_out = (n_in * up)
    n_out = ((n_out // down) + bool((n_out % down)))
    if isinstance(window, (list, np.ndarray)):
        window = np.array(window)
        if (window.ndim > 1):
            raise ValueError('window must be 1-D')
        half_len = ((window.size - 1) // 2)
        h = window
    else:
        max_rate = max(up, down)
        f_c = (1.0 / max_rate)
        half_len = (10 * max_rate)
        h = firwin(((2 * half_len) + 1), f_c, window=window)
    h *= up
    n_pre_pad = (down - (half_len % down))
    n_post_pad = 0
    n_pre_remove = ((half_len + n_pre_pad) // down)
    while (_output_len(((len(h) + n_pre_pad) + n_post_pad), n_in, up, down) < (n_out + n_pre_remove)):
        n_post_pad += 1
    h = np.concatenate((np.zeros(n_pre_pad, dtype=h.dtype), h, np.zeros(n_post_pad, dtype=h.dtype)))
    n_pre_remove_end = (n_pre_remove + n_out)
    funcs = {
        'mean': np.mean,
        'median': np.median,
        'minimum': np.amin,
        'maximum': np.amax,
    }
    upfirdn_kwargs = {
        'mode': 'constant',
        'cval': 0,
    }
    if (padtype in funcs):
        background_values = funcs[padtype](x, axis=axis, keepdims=True)
    elif (padtype in _upfirdn_modes):
        upfirdn_kwargs = {
            'mode': padtype,
        }
        if (padtype == 'constant'):
            if (cval is None):
                cval = 0
            upfirdn_kwargs['cval'] = cval
    else:
        raise ValueError(('padtype must be one of: maximum, mean, median, minimum, ' + ', '.join(_upfirdn_modes)))
    if (padtype in funcs):
        x = (x - background_values)
    y = upfirdn(h, x, up, down, axis=axis, **upfirdn_kwargs)
    keep = ([slice(None)] * x.ndim)
    keep[axis] = slice(n_pre_remove, n_pre_remove_end)
    y_keep = y[tuple(keep)]
    if (padtype in funcs):
        y_keep += background_values
    return y_keep