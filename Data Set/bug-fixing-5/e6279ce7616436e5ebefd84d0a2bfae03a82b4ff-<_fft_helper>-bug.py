def _fft_helper(x, win, detrend_func, nperseg, noverlap, nfft, sides):
    '\n    Calculate windowed FFT, for internal use by\n    scipy.signal._spectral_helper\n\n    This is a helper function that does the main FFT calculation for\n    `_spectral helper`. All input valdiation is performed there, and the\n    data axis is assumed to be the last axis of x. It is not designed to\n    be called externally. The windows are not averaged over; the result\n    from each window is returned.\n\n    Returns\n    -------\n    result : ndarray\n        Array of FFT data\n\n    References\n    ----------\n    .. [1] Stack Overflow, "Repeat NumPy array without replicating\n           data?", http://stackoverflow.com/a/5568169\n\n    Notes\n    -----\n    Adapted from matplotlib.mlab\n\n    .. versionadded:: 0.16.0\n    '
    if ((nperseg == 1) and (noverlap == 0)):
        result = x[(..., np.newaxis)]
    else:
        step = (nperseg - noverlap)
        shape = (x.shape[:(- 1)] + (((x.shape[(- 1)] - noverlap) // step), nperseg))
        strides = (x.strides[:(- 1)] + ((step * x.strides[(- 1)]), x.strides[(- 1)]))
        result = np.lib.stride_tricks.as_strided(x, shape=shape, strides=strides)
    result = detrend_func(result)
    result = (win * result)
    if (sides == 'twosided'):
        func = fftpack.fft
    else:
        result = result.real
        func = np.fft.rfft
    result = func(result, n=nfft)
    return result