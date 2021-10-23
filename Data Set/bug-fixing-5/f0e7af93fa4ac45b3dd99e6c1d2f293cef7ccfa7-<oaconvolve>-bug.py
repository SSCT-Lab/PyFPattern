def oaconvolve(in1, in2, mode='full', axes=None):
    'Convolve two N-dimensional arrays using the overlap-add method.\n\n    Convolve `in1` and `in2` using the overlap-add method, with\n    the output size determined by the `mode` argument.\n\n    This is generally much faster than `convolve` for large arrays (n > ~500),\n    and generally much faster than `fftconvolve` when one array is much\n    larger than the other, but can be slower when only a few output values are\n    needed or when the arrays are very similar in shape, and can only\n    output float arrays (int or object array inputs will be cast to float).\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {\'full\', \'valid\', \'same\'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear convolution\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In \'valid\' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the \'full\' output.\n    axes : int or array_like of ints or None, optional\n        Axes over which to compute the convolution.\n        The default is over all axes.\n\n    Returns\n    -------\n    out : array\n        An N-dimensional array containing a subset of the discrete linear\n        convolution of `in1` with `in2`.\n\n    See Also\n    --------\n    convolve : Uses the direct convolution or FFT convolution algorithm\n               depending on which is faster.\n    fftconvolve : An implementation of convolution using FFT.\n\n    Notes\n    -----\n    .. versionadded:: 1.4.0\n\n    Examples\n    --------\n    Convolve a 100,000 sample signal with a 512-sample filter.\n\n    >>> from scipy import signal\n    >>> sig = np.random.randn(100000)\n    >>> filt = signal.firwin(512, 0.01)\n    >>> fsig = signal.oaconvolve(sig, filt)\n\n    >>> import matplotlib.pyplot as plt\n    >>> fig, (ax_orig, ax_mag) = plt.subplots(2, 1)\n    >>> ax_orig.plot(sig)\n    >>> ax_orig.set_title(\'White noise\')\n    >>> ax_mag.plot(fsig)\n    >>> ax_mag.set_title(\'Filtered noise\')\n    >>> fig.tight_layout()\n    >>> fig.show()\n\n    References\n    ----------\n    .. [1] Wikipedia, "Overlap-add_method".\n           https://en.wikipedia.org/wiki/Overlap-add_method\n    .. [2] Richard G. Lyons. Understanding Digital Signal Processing,\n           Third Edition, 2011. Chapter 13.10.\n           ISBN 13: 978-0137-02741-5\n\n    '
    in1 = asarray(in1)
    in2 = asarray(in2)
    if (in1.ndim == in2.ndim == 0):
        return (in1 * in2)
    elif (in1.ndim != in2.ndim):
        raise ValueError('in1 and in2 should have the same dimensionality')
    elif ((in1.size == 0) or (in2.size == 0)):
        return array([])
    elif (in1.shape == in2.shape):
        return fftconvolve(in1, in2, mode=mode, axes=axes)
    (in1, in2, axes) = _init_freq_conv_axes(in1, in2, mode, axes, sorted_axes=True)
    if (not axes):
        return (in1 * in2)
    s1 = in1.shape
    s2 = in2.shape
    shape_final = [(None if (i not in axes) else ((s1[i] + s2[i]) - 1)) for i in range(in1.ndim)]
    optimal_sizes = ((((- 1), (- 1), s1[i], s2[i]) if (i not in axes) else _calc_oa_lens(s1[i], s2[i])) for i in range(in1.ndim))
    (block_size, overlaps, in1_step, in2_step) = zip(*optimal_sizes)
    if ((in1_step == s1) and (in2_step == s2)):
        return fftconvolve(in1, in2, mode=mode, axes=axes)
    nsteps1 = []
    nsteps2 = []
    pad_size1 = []
    pad_size2 = []
    for i in range(in1.ndim):
        if (i not in axes):
            pad_size1 += [(0, 0)]
            pad_size2 += [(0, 0)]
            continue
        if (s1[i] > in1_step[i]):
            curnstep1 = math.ceil(((s1[i] + 1) / in1_step[i]))
            if (((block_size[i] - overlaps[i]) * curnstep1) < shape_final[i]):
                curnstep1 += 1
            curpad1 = ((curnstep1 * in1_step[i]) - s1[i])
        else:
            curnstep1 = 1
            curpad1 = 0
        if (s2[i] > in2_step[i]):
            curnstep2 = math.ceil(((s2[i] + 1) / in2_step[i]))
            if (((block_size[i] - overlaps[i]) * curnstep2) < shape_final[i]):
                curnstep2 += 1
            curpad2 = ((curnstep2 * in2_step[i]) - s2[i])
        else:
            curnstep2 = 1
            curpad2 = 0
        nsteps1 += [curnstep1]
        nsteps2 += [curnstep2]
        pad_size1 += [(0, curpad1)]
        pad_size2 += [(0, curpad2)]
    if (not all(((curpad == (0, 0)) for curpad in pad_size1))):
        in1 = np.pad(in1, pad_size1, mode='constant', constant_values=0)
    if (not all(((curpad == (0, 0)) for curpad in pad_size2))):
        in2 = np.pad(in2, pad_size2, mode='constant', constant_values=0)
    split_axes = [(iax + i) for (i, iax) in enumerate(axes)]
    fft_axes = [(iax + 1) for iax in split_axes]
    reshape_size1 = list(in1_step)
    reshape_size2 = list(in2_step)
    for (i, iax) in enumerate(split_axes):
        reshape_size1.insert(iax, nsteps1[i])
        reshape_size2.insert(iax, nsteps2[i])
    in1 = in1.reshape(*reshape_size1)
    in2 = in2.reshape(*reshape_size2)
    fft_shape = [block_size[i] for i in axes]
    ret = _freq_domain_conv(in1, in2, fft_axes, fft_shape, calc_fast_len=False)
    for (ax, ax_fft, ax_split) in zip(axes, fft_axes, split_axes):
        overlap = overlaps[ax]
        if (overlap is None):
            continue
        (ret, overpart) = np.split(ret, [(- overlap)], ax_fft)
        overpart = np.split(overpart, [(- 1)], ax_split)[0]
        ret_overpart = np.split(ret, [overlap], ax_fft)[0]
        ret_overpart = np.split(ret_overpart, [1], ax_split)[1]
        ret_overpart += overpart
    shape_ret = [(ret.shape[i] if (i not in fft_axes) else (ret.shape[i] * ret.shape[(i - 1)])) for i in range(ret.ndim) if (i not in split_axes)]
    ret = ret.reshape(*shape_ret)
    slice_final = tuple([slice(islice) for islice in shape_final])
    ret = ret[slice_final]
    return _apply_conv_mode(ret, s1, s2, mode, axes)