def fftconvolve(in1, in2, mode='full', axes=None):
    "Convolve two N-dimensional arrays using FFT.\n\n    Convolve `in1` and `in2` using the fast Fourier transform method, with\n    the output size determined by the `mode` argument.\n\n    This is generally much faster than `convolve` for large arrays (n > ~500),\n    but can be slower when only a few output values are needed, and can only\n    output float arrays (int or object array inputs will be cast to float).\n\n    As of v0.19, `convolve` automatically chooses this method or the direct\n    method based on an estimation of which is faster.\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear convolution\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    axes : int or array_like of ints or None, optional\n        Axes over which to compute the convolution.\n        The default is over all axes.\n\n    Returns\n    -------\n    out : array\n        An N-dimensional array containing a subset of the discrete linear\n        convolution of `in1` with `in2`.\n\n    See Also\n    --------\n    convolve : Uses the direct convolution or FFT convolution algorithm\n               depending on which is faster.\n    oaconvolve : Uses the overlap-add method to do convolution, which is\n                 generally faster when the input arrays are large and\n                 significantly different in size.\n\n    Examples\n    --------\n    Autocorrelation of white noise is an impulse.\n\n    >>> from scipy import signal\n    >>> sig = np.random.randn(1000)\n    >>> autocorr = signal.fftconvolve(sig, sig[::-1], mode='full')\n\n    >>> import matplotlib.pyplot as plt\n    >>> fig, (ax_orig, ax_mag) = plt.subplots(2, 1)\n    >>> ax_orig.plot(sig)\n    >>> ax_orig.set_title('White noise')\n    >>> ax_mag.plot(np.arange(-len(sig)+1,len(sig)), autocorr)\n    >>> ax_mag.set_title('Autocorrelation')\n    >>> fig.tight_layout()\n    >>> fig.show()\n\n    Gaussian blur implemented using FFT convolution.  Notice the dark borders\n    around the image, due to the zero-padding beyond its boundaries.\n    The `convolve2d` function allows for other types of image boundaries,\n    but is far slower.\n\n    >>> from scipy import misc\n    >>> face = misc.face(gray=True)\n    >>> kernel = np.outer(signal.gaussian(70, 8), signal.gaussian(70, 8))\n    >>> blurred = signal.fftconvolve(face, kernel, mode='same')\n\n    >>> fig, (ax_orig, ax_kernel, ax_blurred) = plt.subplots(3, 1,\n    ...                                                      figsize=(6, 15))\n    >>> ax_orig.imshow(face, cmap='gray')\n    >>> ax_orig.set_title('Original')\n    >>> ax_orig.set_axis_off()\n    >>> ax_kernel.imshow(kernel, cmap='gray')\n    >>> ax_kernel.set_title('Gaussian kernel')\n    >>> ax_kernel.set_axis_off()\n    >>> ax_blurred.imshow(blurred, cmap='gray')\n    >>> ax_blurred.set_title('Blurred')\n    >>> ax_blurred.set_axis_off()\n    >>> fig.show()\n\n    "
    in1 = asarray(in1)
    in2 = asarray(in2)
    if (in1.ndim == in2.ndim == 0):
        return (in1 * in2)
    elif (in1.ndim != in2.ndim):
        raise ValueError('in1 and in2 should have the same dimensionality')
    elif ((in1.size == 0) or (in2.size == 0)):
        return array([])
    (in1, in2, axes) = _init_freq_conv_axes(in1, in2, mode, axes, sorted_axes=False)
    s1 = in1.shape
    s2 = in2.shape
    shape = [(max((s1[i], s2[i])) if (i not in axes) else ((s1[i] + s2[i]) - 1)) for i in range(in1.ndim)]
    ret = _freq_domain_conv(in1, in2, axes, shape, calc_fast_len=True)
    return _apply_conv_mode(ret, s1, s2, mode, axes)