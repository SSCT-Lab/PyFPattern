def correlate2d(in1, in2, mode='full', boundary='fill', fillvalue=0):
    "\n    Cross-correlate two 2-dimensional arrays.\n\n    Cross correlate `in1` and `in2` with output size determined by `mode`, and\n    boundary conditions determined by `boundary` and `fillvalue`.\n\n    Parameters\n    ----------\n    in1 : array_like\n        First input.\n    in2 : array_like\n        Second input. Should have the same number of dimensions as `in1`.\n    mode : str {'full', 'valid', 'same'}, optional\n        A string indicating the size of the output:\n\n        ``full``\n           The output is the full discrete linear cross-correlation\n           of the inputs. (Default)\n        ``valid``\n           The output consists only of those elements that do not\n           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`\n           must be at least as large as the other in every dimension.\n        ``same``\n           The output is the same size as `in1`, centered\n           with respect to the 'full' output.\n    boundary : str {'fill', 'wrap', 'symm'}, optional\n        A flag indicating how to handle boundaries:\n\n        ``fill``\n           pad input arrays with fillvalue. (default)\n        ``wrap``\n           circular boundary conditions.\n        ``symm``\n           symmetrical boundary conditions.\n\n    fillvalue : scalar, optional\n        Value to fill pad input arrays with. Default is 0.\n\n    Returns\n    -------\n    correlate2d : ndarray\n        A 2-dimensional array containing a subset of the discrete linear\n        cross-correlation of `in1` with `in2`.\n\n    Examples\n    --------\n    Use 2D cross-correlation to find the location of a template in a noisy\n    image:\n\n    >>> from scipy import signal\n    >>> from scipy import misc\n    >>> face = misc.face(gray=True) - misc.face(gray=True).mean()\n    >>> template = np.copy(face[300:365, 670:750])  # right eye\n    >>> template -= template.mean()\n    >>> face = face + np.random.randn(*face.shape) * 50  # add noise\n    >>> corr = signal.correlate2d(face, template, boundary='symm', mode='same')\n    >>> y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match\n\n    >>> import matplotlib.pyplot as plt\n    >>> fig, (ax_orig, ax_template, ax_corr) = plt.subplots(3, 1,\n    ...                                                     figsize=(6, 15))\n    >>> ax_orig.imshow(face, cmap='gray')\n    >>> ax_orig.set_title('Original')\n    >>> ax_orig.set_axis_off()\n    >>> ax_template.imshow(template, cmap='gray')\n    >>> ax_template.set_title('Template')\n    >>> ax_template.set_axis_off()\n    >>> ax_corr.imshow(corr, cmap='gray')\n    >>> ax_corr.set_title('Cross-correlation')\n    >>> ax_corr.set_axis_off()\n    >>> ax_orig.plot(x, y, 'ro')\n    >>> fig.show()\n\n    "
    in1 = asarray(in1)
    in2 = asarray(in2)
    if (not (in1.ndim == in2.ndim == 2)):
        raise ValueError('correlate2d inputs must both be 2D arrays')
    swapped_inputs = _inputs_swap_needed(mode, in1.shape, in2.shape)
    if swapped_inputs:
        (in1, in2) = (in2, in1)
    val = _valfrommode(mode)
    bval = _bvalfromboundary(boundary)
    out = sigtools._convolve2d(in1, in2.conj(), 0, val, bval, fillvalue)
    if swapped_inputs:
        out = out[::(- 1), ::(- 1)]
    return out