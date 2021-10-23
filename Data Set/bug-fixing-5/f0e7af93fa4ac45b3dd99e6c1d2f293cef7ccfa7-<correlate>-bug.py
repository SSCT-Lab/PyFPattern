def correlate(in1, in2, mode='full', method='auto'):
    "\n    Cross-correlate two N-dimensional arrays.\n\n    Cross-correlate `in1` and `in2`, with the output size determined by the\n    `mode` argument.\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear cross-correlation\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    method : str {'auto', 'direct', 'fft'}, optional\n        A string indicating which method to use to calculate the correlation.\n\n        ``direct``\n           The correlation is determined directly from sums, the definition of\n           correlation.\n        ``fft``\n           The Fast Fourier Transform is used to perform the correlation more\n           quickly (only available for numerical arrays.)\n        ``auto``\n           Automatically chooses direct or Fourier method based on an estimate\n           of which is faster (default).  See `convolve` Notes for more detail.\n\n           .. versionadded:: 0.19.0\n\n    Returns\n    -------\n    correlate : array\n        An N-dimensional array containing a subset of the discrete linear\n        cross-correlation of `in1` with `in2`.\n\n    See Also\n    --------\n    choose_conv_method : contains more documentation on `method`.\n\n    Notes\n    -----\n    The correlation z of two d-dimensional arrays x and y is defined as::\n\n        z[...,k,...] = sum[..., i_l, ...] x[..., i_l,...] * conj(y[..., i_l - k,...])\n\n    This way, if x and y are 1-D arrays and ``z = correlate(x, y, 'full')``\n    then\n\n    .. math::\n\n          z[k] = (x * y)(k - N + 1)\n               = \\sum_{l=0}^{||x||-1}x_l y_{l-k+N-1}^{*}\n\n    for :math:`k = 0, 1, ..., ||x|| + ||y|| - 2`\n\n    where :math:`||x||` is the length of ``x``, :math:`N = \\max(||x||,||y||)`,\n    and :math:`y_m` is 0 when m is outside the range of y.\n\n    ``method='fft'`` only works for numerical arrays as it relies on\n    `fftconvolve`. In certain cases (i.e., arrays of objects or when\n    rounding integers can lose precision), ``method='direct'`` is always used.\n\n    Examples\n    --------\n    Implement a matched filter using cross-correlation, to recover a signal\n    that has passed through a noisy channel.\n\n    >>> from scipy import signal\n    >>> sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)\n    >>> sig_noise = sig + np.random.randn(len(sig))\n    >>> corr = signal.correlate(sig_noise, np.ones(128), mode='same') / 128\n\n    >>> import matplotlib.pyplot as plt\n    >>> clock = np.arange(64, len(sig), 128)\n    >>> fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)\n    >>> ax_orig.plot(sig)\n    >>> ax_orig.plot(clock, sig[clock], 'ro')\n    >>> ax_orig.set_title('Original signal')\n    >>> ax_noise.plot(sig_noise)\n    >>> ax_noise.set_title('Signal with noise')\n    >>> ax_corr.plot(corr)\n    >>> ax_corr.plot(clock, corr[clock], 'ro')\n    >>> ax_corr.axhline(0.5, ls=':')\n    >>> ax_corr.set_title('Cross-correlated with rectangular pulse')\n    >>> ax_orig.margins(0, 0.1)\n    >>> fig.tight_layout()\n    >>> fig.show()\n\n    "
    in1 = asarray(in1)
    in2 = asarray(in2)
    if (in1.ndim == in2.ndim == 0):
        return (in1 * in2.conj())
    elif (in1.ndim != in2.ndim):
        raise ValueError('in1 and in2 should have the same dimensionality')
    try:
        val = _modedict[mode]
    except KeyError:
        raise ValueError("Acceptable mode flags are 'valid', 'same', or 'full'.")
    if (method in ('fft', 'auto')):
        return convolve(in1, _reverse_and_conj(in2), mode, method)
    elif (method == 'direct'):
        if _np_conv_ok(in1, in2, mode):
            return np.correlate(in1, in2, mode)
        swapped_inputs = (((mode == 'full') and (in2.size > in1.size)) or _inputs_swap_needed(mode, in1.shape, in2.shape))
        if swapped_inputs:
            (in1, in2) = (in2, in1)
        if (mode == 'valid'):
            ps = [((i - j) + 1) for (i, j) in zip(in1.shape, in2.shape)]
            out = np.empty(ps, in1.dtype)
            z = sigtools._correlateND(in1, in2, out, val)
        else:
            ps = [((i + j) - 1) for (i, j) in zip(in1.shape, in2.shape)]
            in1zpadded = np.zeros(ps, in1.dtype)
            sc = tuple((slice(0, i) for i in in1.shape))
            in1zpadded[sc] = in1.copy()
            if (mode == 'full'):
                out = np.empty(ps, in1.dtype)
            elif (mode == 'same'):
                out = np.empty(in1.shape, in1.dtype)
            z = sigtools._correlateND(in1zpadded, in2, out, val)
        if swapped_inputs:
            z = _reverse_and_conj(z)
        return z
    else:
        raise ValueError("Acceptable method flags are 'auto', 'direct', or 'fft'.")