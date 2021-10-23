def resample(x, num, t=None, axis=0, window=None):
    "\n    Resample `x` to `num` samples using Fourier method along the given axis.\n\n    The resampled signal starts at the same value as `x` but is sampled\n    with a spacing of ``len(x) / num * (spacing of x)``.  Because a\n    Fourier method is used, the signal is assumed to be periodic.\n\n    Parameters\n    ----------\n    x : array_like\n        The data to be resampled.\n    num : int\n        The number of samples in the resampled signal.\n    t : array_like, optional\n        If `t` is given, it is assumed to be the equally spaced sample\n        positions associated with the signal data in `x`.\n    axis : int, optional\n        The axis of `x` that is resampled.  Default is 0.\n    window : array_like, callable, string, float, or tuple, optional\n        Specifies the window applied to the signal in the Fourier\n        domain.  See below for details.\n\n    Returns\n    -------\n    resampled_x or (resampled_x, resampled_t)\n        Either the resampled array, or, if `t` was given, a tuple\n        containing the resampled array and the corresponding resampled\n        positions.\n\n    See Also\n    --------\n    decimate : Downsample the signal after applying an FIR or IIR filter.\n    resample_poly : Resample using polyphase filtering and an FIR filter.\n\n    Notes\n    -----\n    The argument `window` controls a Fourier-domain window that tapers\n    the Fourier spectrum before zero-padding to alleviate ringing in\n    the resampled values for sampled signals you didn't intend to be\n    interpreted as band-limited.\n\n    If `window` is a function, then it is called with a vector of inputs\n    indicating the frequency bins (i.e. fftfreq(x.shape[axis]) ).\n\n    If `window` is an array of the same length as `x.shape[axis]` it is\n    assumed to be the window to be applied directly in the Fourier\n    domain (with dc and low-frequency first).\n\n    For any other type of `window`, the function `scipy.signal.get_window`\n    is called to generate the window.\n\n    The first sample of the returned vector is the same as the first\n    sample of the input vector.  The spacing between samples is changed\n    from ``dx`` to ``dx * len(x) / num``.\n\n    If `t` is not None, then it is used solely to calculate the resampled\n    positions `resampled_t`\n\n    As noted, `resample` uses FFT transformations, which can be very\n    slow if the number of input or output samples is large and prime;\n    see `scipy.fft.fft`.\n\n    Examples\n    --------\n    Note that the end of the resampled data rises to meet the first\n    sample of the next cycle:\n\n    >>> from scipy import signal\n\n    >>> x = np.linspace(0, 10, 20, endpoint=False)\n    >>> y = np.cos(-x**2/6.0)\n    >>> f = signal.resample(y, 100)\n    >>> xnew = np.linspace(0, 10, 100, endpoint=False)\n\n    >>> import matplotlib.pyplot as plt\n    >>> plt.plot(x, y, 'go-', xnew, f, '.-', 10, y[0], 'ro')\n    >>> plt.legend(['data', 'resampled'], loc='best')\n    >>> plt.show()\n    "
    x = np.asarray(x)
    X = sp_fft.fft(x, axis=axis)
    Nx = x.shape[axis]
    real_input = np.isrealobj(x)
    if real_input:
        X = sp_fft.rfft(x, axis=axis)
    else:
        X = sp_fft.fft(x, axis=axis)
    if (window is not None):
        if callable(window):
            W = window(sp_fft.fftfreq(Nx))
        elif isinstance(window, np.ndarray):
            if (window.shape != (Nx,)):
                raise ValueError('window must have the same length as data')
            W = window
        else:
            W = sp_fft.ifftshift(get_window(window, Nx))
        newshape_W = ([1] * x.ndim)
        newshape_W[axis] = X.shape[axis]
        if real_input:
            W_real = W.copy()
            W_real[1:] += W_real[(- 1):0:(- 1)]
            W_real[1:] *= 0.5
            X *= W_real[:newshape_W[axis]].reshape(newshape_W)
        else:
            X *= W.reshape(newshape_W)
    newshape = list(x.shape)
    if real_input:
        newshape[axis] = ((num // 2) + 1)
    else:
        newshape[axis] = num
    Y = np.zeros(newshape, X.dtype)
    N = min(num, Nx)
    nyq = ((N // 2) + 1)
    sl = ([slice(None)] * x.ndim)
    sl[axis] = slice(0, nyq)
    Y[tuple(sl)] = X[tuple(sl)]
    if (not real_input):
        if (N > 2):
            sl[axis] = slice((nyq - N), None)
            Y[tuple(sl)] = X[tuple(sl)]
    if ((N % 2) == 0):
        if (num < Nx):
            if real_input:
                sl[axis] = slice((N // 2), ((N // 2) + 1))
                Y[tuple(sl)] *= 2.0
            else:
                sl[axis] = slice(((- N) // 2), (((- N) // 2) + 1))
                Y[tuple(sl)] += X[tuple(sl)]
        elif (Nx < num):
            sl[axis] = slice((N // 2), ((N // 2) + 1))
            Y[tuple(sl)] *= 0.5
            if (not real_input):
                temp = Y[tuple(sl)]
                sl[axis] = slice((num - (N // 2)), ((num - (N // 2)) + 1))
                Y[tuple(sl)] = temp
    if real_input:
        y = sp_fft.irfft(Y, num, axis=axis)
    else:
        y = sp_fft.ifft(Y, axis=axis, overwrite_x=True)
    y *= (float(num) / float(Nx))
    if (t is None):
        return y
    else:
        new_t = ((((np.arange(0, num) * (t[1] - t[0])) * Nx) / float(num)) + t[0])
        return (y, new_t)