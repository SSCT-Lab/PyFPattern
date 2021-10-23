def convolve(in1, in2, mode='full', method='auto'):
    "\n    Convolve two N-dimensional arrays.\n\n    Convolve `in1` and `in2`, with the output size determined by the\n    `mode` argument.\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear convolution\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    method : str {'auto', 'direct', 'fft'}, optional\n        A string indicating which method to use to calculate the convolution.\n\n        ``direct``\n           The convolution is determined directly from sums, the definition of\n           convolution.\n        ``fft``\n           The Fourier Transform is used to perform the convolution by calling\n           `fftconvolve`.\n        ``auto``\n           Automatically chooses direct or Fourier method based on an estimate\n           of which is faster (default).  See Notes for more detail.\n\n           .. versionadded:: 0.19.0\n\n    Returns\n    -------\n    convolve : array\n        An N-dimensional array containing a subset of the discrete linear\n        convolution of `in1` with `in2`.\n\n    See Also\n    --------\n    numpy.polymul : performs polynomial multiplication (same operation, but\n                    also accepts poly1d objects)\n    choose_conv_method : chooses the fastest appropriate convolution method\n    fftconvolve : Always uses the FFT method.\n    oaconvolve : Uses the overlap-add method to do convolution, which is\n                 generally faster when the input arrays are large and\n                 significantly different in size.\n\n    Notes\n    -----\n    By default, `convolve` and `correlate` use ``method='auto'``, which calls\n    `choose_conv_method` to choose the fastest method using pre-computed\n    values (`choose_conv_method` can also measure real-world timing with a\n    keyword argument). Because `fftconvolve` relies on floating point numbers,\n    there are certain constraints that may force `method=direct` (more detail\n    in `choose_conv_method` docstring).\n\n    Examples\n    --------\n    Smooth a square pulse using a Hann window:\n\n    >>> from scipy import signal\n    >>> sig = np.repeat([0., 1., 0.], 100)\n    >>> win = signal.hann(50)\n    >>> filtered = signal.convolve(sig, win, mode='same') / sum(win)\n\n    >>> import matplotlib.pyplot as plt\n    >>> fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True)\n    >>> ax_orig.plot(sig)\n    >>> ax_orig.set_title('Original pulse')\n    >>> ax_orig.margins(0, 0.1)\n    >>> ax_win.plot(win)\n    >>> ax_win.set_title('Filter impulse response')\n    >>> ax_win.margins(0, 0.1)\n    >>> ax_filt.plot(filtered)\n    >>> ax_filt.set_title('Filtered signal')\n    >>> ax_filt.margins(0, 0.1)\n    >>> fig.tight_layout()\n    >>> fig.show()\n\n    "
    volume = np.asarray(in1)
    kernel = np.asarray(in2)
    if (volume.ndim == kernel.ndim == 0):
        return (volume * kernel)
    elif (volume.ndim != kernel.ndim):
        raise ValueError('volume and kernel should have the same dimensionality')
    if _inputs_swap_needed(mode, volume.shape, kernel.shape):
        (volume, kernel) = (kernel, volume)
    if (method == 'auto'):
        method = choose_conv_method(volume, kernel, mode=mode)
    if (method == 'fft'):
        out = fftconvolve(volume, kernel, mode=mode)
        result_type = np.result_type(volume, kernel)
        if (result_type.kind in {'u', 'i'}):
            out = np.around(out)
        return out.astype(result_type)
    elif (method == 'direct'):
        if _np_conv_ok(volume, kernel, mode):
            return np.convolve(volume, kernel, mode)
        return correlate(volume, _reverse_and_conj(kernel), mode, 'direct')
    else:
        raise ValueError("Acceptable method flags are 'auto', 'direct', or 'fft'.")