def convolve2d(in1, in2, mode='full', boundary='fill', fillvalue=0):
    "\n    Convolve two 2-dimensional arrays.\n\n    Convolve `in1` and `in2` with output size determined by `mode`, and\n    boundary conditions determined by `boundary` and `fillvalue`.\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear convolution\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    boundary : str {'fill', 'wrap', 'symm'}, optional\n        A flag indicating how to handle boundaries:\n\n        ``fill``\n           pad input arrays with fillvalue. (default)\n        ``wrap``\n           circular boundary conditions.\n        ``symm``\n           symmetrical boundary conditions.\n\n    fillvalue : scalar, optional\n        Value to fill pad input arrays with. Default is 0.\n\n    Returns\n    -------\n    out : ndarray\n        A 2-dimensional array containing a subset of the discrete linear\n        convolution of `in1` with `in2`.\n\n    Examples\n    --------\n    Compute the gradient of an image by 2D convolution with a complex Scharr\n    operator.  (Horizontal operator is real, vertical is imaginary.)  Use\n    symmetric boundary condition to avoid creating edges at the image\n    boundaries.\n\n    >>> from scipy import signal\n    >>> from scipy import misc\n    >>> ascent = misc.ascent()\n    >>> scharr = np.array([[ -3-3j, 0-10j,  +3 -3j],\n    ...                    [-10+0j, 0+ 0j, +10 +0j],\n    ...                    [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy\n    >>> grad = signal.convolve2d(ascent, scharr, boundary='symm', mode='same')\n\n    >>> import matplotlib.pyplot as plt\n    >>> fig, (ax_orig, ax_mag, ax_ang) = plt.subplots(3, 1, figsize=(6, 15))\n    >>> ax_orig.imshow(ascent, cmap='gray')\n    >>> ax_orig.set_title('Original')\n    >>> ax_orig.set_axis_off()\n    >>> ax_mag.imshow(np.absolute(grad), cmap='gray')\n    >>> ax_mag.set_title('Gradient magnitude')\n    >>> ax_mag.set_axis_off()\n    >>> ax_ang.imshow(np.angle(grad), cmap='hsv') # hsv is cyclic, like angles\n    >>> ax_ang.set_title('Gradient orientation')\n    >>> ax_ang.set_axis_off()\n    >>> fig.show()\n\n    "
    in1 = np.asarray(in1)
    in2 = np.asarray(in2)
    if (not (in1.ndim == in2.ndim == 2)):
        raise ValueError('convolve2d inputs must both be 2D arrays')
    if _inputs_swap_needed(mode, in1.shape, in2.shape):
        (in1, in2) = (in2, in1)
    val = _valfrommode(mode)
    bval = _bvalfromboundary(boundary)
    out = sigtools._convolve2d(in1, in2, 1, val, bval, fillvalue)
    return out