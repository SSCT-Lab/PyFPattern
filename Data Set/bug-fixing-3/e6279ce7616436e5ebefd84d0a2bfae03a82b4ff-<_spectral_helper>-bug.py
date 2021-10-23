def _spectral_helper(x, y, fs=1.0, window='hann', nperseg=None, noverlap=None, nfft=None, detrend='constant', return_onesided=True, scaling='spectrum', axis=(- 1), mode='psd', boundary=None, padded=False):
    '\n    Calculate various forms of windowed FFTs for PSD, CSD, etc.\n\n    This is a helper function that implements the commonality between\n    the stft, psd, csd, and spectrogram functions. It is not designed to\n    be called externally. The windows are not averaged over; the result\n    from each window is returned.\n\n    Parameters\n    ---------\n    x : array_like\n        Array or sequence containing the data to be analyzed.\n    y : array_like\n        Array or sequence containing the data to be analyzed. If this is\n        the same object in memory as `x` (i.e. ``_spectral_helper(x,\n        x, ...)``), the extra computations are spared.\n    fs : float, optional\n        Sampling frequency of the time series. Defaults to 1.0.\n    window : str or tuple or array_like, optional\n        Desired window to use. If `window` is a string or tuple, it is\n        passed to `get_window` to generate the window values, which are\n        DFT-even by default. See `get_window` for a list of windows and\n        required parameters. If `window` is array_like it will be used\n        directly as the window and its length must be nperseg. Defaults\n        to a Hann window.\n    nperseg : int, optional\n        Length of each segment. Defaults to None, but if window is str or\n        tuple, is set to 256, and if window is array_like, is set to the\n        length of the window.\n    noverlap : int, optional\n        Number of points to overlap between segments. If `None`,\n        ``noverlap = nperseg // 2``. Defaults to `None`.\n    nfft : int, optional\n        Length of the FFT used, if a zero padded FFT is desired. If\n        `None`, the FFT length is `nperseg`. Defaults to `None`.\n    detrend : str or function or `False`, optional\n        Specifies how to detrend each segment. If `detrend` is a\n        string, it is passed as the `type` argument to the `detrend`\n        function. If it is a function, it takes a segment and returns a\n        detrended segment. If `detrend` is `False`, no detrending is\n        done. Defaults to \'constant\'.\n    return_onesided : bool, optional\n        If `True`, return a one-sided spectrum for real data. If\n        `False` return a two-sided spectrum. Note that for complex\n        data, a two-sided spectrum is always returned.\n    scaling : { \'density\', \'spectrum\' }, optional\n        Selects between computing the cross spectral density (\'density\')\n        where `Pxy` has units of V**2/Hz and computing the cross\n        spectrum (\'spectrum\') where `Pxy` has units of V**2, if `x`\n        and `y` are measured in V and `fs` is measured in Hz.\n        Defaults to \'density\'\n    axis : int, optional\n        Axis along which the FFTs are computed; the default is over the\n        last axis (i.e. ``axis=-1``).\n    mode: str {\'psd\', \'stft\'}, optional\n        Defines what kind of return values are expected. Defaults to\n        \'psd\'.\n    boundary : str or None, optional\n        Specifies whether the input signal is extended at both ends, and\n        how to generate the new values, in order to center the first\n        windowed segment on the first input point. This has the benefit\n        of enabling reconstruction of the first input point when the\n        employed window function starts at zero. Valid options are\n        ``[\'even\', \'odd\', \'constant\', \'zeros\', None]``. Defaults to\n        `None`.\n    padded : bool, optional\n        Specifies whether the input signal is zero-padded at the end to\n        make the signal fit exactly into an integer number of window\n        segments, so that all of the signal is included in the output.\n        Defaults to `False`. Padding occurs after boundary extension, if\n        `boundary` is not `None`, and `padded` is `True`.\n    Returns\n    -------\n    freqs : ndarray\n        Array of sample frequencies.\n    t : ndarray\n        Array of times corresponding to each data segment\n    result : ndarray\n        Array of output data, contents dependent on *mode* kwarg.\n\n    References\n    ----------\n    .. [1] Stack Overflow, "Rolling window for 1D arrays in Numpy?",\n           http://stackoverflow.com/a/6811241\n    .. [2] Stack Overflow, "Using strides for an efficient moving\n           average filter", http://stackoverflow.com/a/4947453\n\n    Notes\n    -----\n    Adapted from matplotlib.mlab\n\n    .. versionadded:: 0.16.0\n    '
    if (mode not in ['psd', 'stft']):
        raise ValueError(("Unknown value for mode %s, must be one of: {'psd', 'stft'}" % mode))
    boundary_funcs = {
        'even': even_ext,
        'odd': odd_ext,
        'constant': const_ext,
        'zeros': zero_ext,
        None: None,
    }
    if (boundary not in boundary_funcs):
        raise ValueError("Unknown boundary option '{0}', must be one of: {1}".format(boundary, list(boundary_funcs.keys())))
    same_data = (y is x)
    if ((not same_data) and (mode != 'psd')):
        raise ValueError("x and y must be equal if mode is 'stft'")
    axis = int(axis)
    x = np.asarray(x)
    if (not same_data):
        y = np.asarray(y)
        outdtype = np.result_type(x, y, np.complex64)
    else:
        outdtype = np.result_type(x, np.complex64)
    if (not same_data):
        xouter = list(x.shape)
        youter = list(y.shape)
        xouter.pop(axis)
        youter.pop(axis)
        try:
            outershape = np.broadcast(np.empty(xouter), np.empty(youter)).shape
        except ValueError:
            raise ValueError('x and y cannot be broadcast together.')
    if same_data:
        if (x.size == 0):
            return (np.empty(x.shape), np.empty(x.shape), np.empty(x.shape))
    elif ((x.size == 0) or (y.size == 0)):
        outshape = (outershape + (min([x.shape[axis], y.shape[axis]]),))
        emptyout = np.rollaxis(np.empty(outshape), (- 1), axis)
        return (emptyout, emptyout, emptyout)
    if (x.ndim > 1):
        if (axis != (- 1)):
            x = np.rollaxis(x, axis, len(x.shape))
            if ((not same_data) and (y.ndim > 1)):
                y = np.rollaxis(y, axis, len(y.shape))
    if (not same_data):
        if (x.shape[(- 1)] != y.shape[(- 1)]):
            if (x.shape[(- 1)] < y.shape[(- 1)]):
                pad_shape = list(x.shape)
                pad_shape[(- 1)] = (y.shape[(- 1)] - x.shape[(- 1)])
                x = np.concatenate((x, np.zeros(pad_shape)), (- 1))
            else:
                pad_shape = list(y.shape)
                pad_shape[(- 1)] = (x.shape[(- 1)] - y.shape[(- 1)])
                y = np.concatenate((y, np.zeros(pad_shape)), (- 1))
    if (nperseg is not None):
        nperseg = int(nperseg)
        if (nperseg < 1):
            raise ValueError('nperseg must be a positive integer')
    (win, nperseg) = _triage_segments(window, nperseg, input_length=x.shape[(- 1)])
    if (nfft is None):
        nfft = nperseg
    elif (nfft < nperseg):
        raise ValueError('nfft must be greater than or equal to nperseg.')
    else:
        nfft = int(nfft)
    if (noverlap is None):
        noverlap = (nperseg // 2)
    else:
        noverlap = int(noverlap)
    if (noverlap >= nperseg):
        raise ValueError('noverlap must be less than nperseg.')
    nstep = (nperseg - noverlap)
    if (boundary is not None):
        ext_func = boundary_funcs[boundary]
        x = ext_func(x, (nperseg // 2), axis=(- 1))
        if (not same_data):
            y = ext_func(y, (nperseg // 2), axis=(- 1))
    if padded:
        nadd = (((- (x.shape[(- 1)] - nperseg)) % nstep) % nperseg)
        zeros_shape = (list(x.shape[:(- 1)]) + [nadd])
        x = np.concatenate((x, np.zeros(zeros_shape)), axis=(- 1))
        if (not same_data):
            zeros_shape = (list(y.shape[:(- 1)]) + [nadd])
            y = np.concatenate((y, np.zeros(zeros_shape)), axis=(- 1))
    if (not detrend):

        def detrend_func(d):
            return d
    elif (not hasattr(detrend, '__call__')):

        def detrend_func(d):
            return signaltools.detrend(d, type=detrend, axis=(- 1))
    elif (axis != (- 1)):

        def detrend_func(d):
            d = np.rollaxis(d, (- 1), axis)
            d = detrend(d)
            return np.rollaxis(d, axis, len(d.shape))
    else:
        detrend_func = detrend
    if (np.result_type(win, np.complex64) != outdtype):
        win = win.astype(outdtype)
    if (scaling == 'density'):
        scale = (1.0 / (fs * (win * win).sum()))
    elif (scaling == 'spectrum'):
        scale = (1.0 / (win.sum() ** 2))
    else:
        raise ValueError(('Unknown scaling: %r' % scaling))
    if (mode == 'stft'):
        scale = np.sqrt(scale)
    if return_onesided:
        if np.iscomplexobj(x):
            sides = 'twosided'
            warnings.warn('Input data is complex, switching to return_onesided=False')
        else:
            sides = 'onesided'
            if (not same_data):
                if np.iscomplexobj(y):
                    sides = 'twosided'
                    warnings.warn('Input data is complex, switching to return_onesided=False')
    else:
        sides = 'twosided'
    if (sides == 'twosided'):
        freqs = fftpack.fftfreq(nfft, (1 / fs))
    elif (sides == 'onesided'):
        freqs = np.fft.rfftfreq(nfft, (1 / fs))
    result = _fft_helper(x, win, detrend_func, nperseg, noverlap, nfft, sides)
    if (not same_data):
        result_y = _fft_helper(y, win, detrend_func, nperseg, noverlap, nfft, sides)
        result = (np.conjugate(result) * result_y)
    elif (mode == 'psd'):
        result = (np.conjugate(result) * result)
    result *= scale
    if ((sides == 'onesided') and (mode == 'psd')):
        if (nfft % 2):
            result[..., 1:] *= 2
        else:
            result[..., 1:(- 1)] *= 2
    time = (np.arange((nperseg / 2), ((x.shape[(- 1)] - (nperseg / 2)) + 1), (nperseg - noverlap)) / float(fs))
    if (boundary is not None):
        time -= ((nperseg / 2) / fs)
    result = result.astype(outdtype)
    if (same_data and (mode != 'stft')):
        result = result.real
    if (axis < 0):
        axis -= 1
    result = np.rollaxis(result, (- 1), axis)
    return (freqs, time, result)