def sosfilt(sos, x, axis=(- 1), zi=None):
    "\n    Filter data along one dimension using cascaded second-order sections.\n\n    Filter a data sequence, `x`, using a digital IIR filter defined by\n    `sos`. This is implemented by performing `lfilter` for each\n    second-order section.  See `lfilter` for details.\n\n    Parameters\n    ----------\n    sos : array_like\n        Array of second-order filter coefficients, must have shape\n        ``(n_sections, 6)``. Each row corresponds to a second-order\n        section, with the first three columns providing the numerator\n        coefficients and the last three providing the denominator\n        coefficients.\n    x : array_like\n        An N-dimensional input array.\n    axis : int, optional\n        The axis of the input data array along which to apply the\n        linear filter. The filter is applied to each subarray along\n        this axis.  Default is -1.\n    zi : array_like, optional\n        Initial conditions for the cascaded filter delays.  It is a (at\n        least 2D) vector of shape ``(n_sections, ..., 2, ...)``, where\n        ``..., 2, ...`` denotes the shape of `x`, but with ``x.shape[axis]``\n        replaced by 2.  If `zi` is None or is not given then initial rest\n        (i.e. all zeros) is assumed.\n        Note that these initial conditions are *not* the same as the initial\n        conditions given by `lfiltic` or `lfilter_zi`.\n\n    Returns\n    -------\n    y : ndarray\n        The output of the digital filter.\n    zf : ndarray, optional\n        If `zi` is None, this is not returned, otherwise, `zf` holds the\n        final filter delay values.\n\n    See Also\n    --------\n    zpk2sos, sos2zpk, sosfilt_zi, sosfiltfilt, sosfreqz\n\n    Notes\n    -----\n    The filter function is implemented as a series of second-order filters\n    with direct-form II transposed structure. It is designed to minimize\n    numerical precision errors for high-order filters.\n\n    .. versionadded:: 0.16.0\n\n    Examples\n    --------\n    Plot a 13th-order filter's impulse response using both `lfilter` and\n    `sosfilt`, showing the instability that results from trying to do a\n    13th-order filter in a single stage (the numerical error pushes some poles\n    outside of the unit circle):\n\n    >>> import matplotlib.pyplot as plt\n    >>> from scipy import signal\n    >>> b, a = signal.ellip(13, 0.009, 80, 0.05, output='ba')\n    >>> sos = signal.ellip(13, 0.009, 80, 0.05, output='sos')\n    >>> x = signal.unit_impulse(700)\n    >>> y_tf = signal.lfilter(b, a, x)\n    >>> y_sos = signal.sosfilt(sos, x)\n    >>> plt.plot(y_tf, 'r', label='TF')\n    >>> plt.plot(y_sos, 'k', label='SOS')\n    >>> plt.legend(loc='best')\n    >>> plt.show()\n\n    "
    x = np.asarray(x)
    (sos, n_sections) = _validate_sos(sos)
    use_zi = (zi is not None)
    if use_zi:
        zi = np.asarray(zi)
        x_zi_shape = list(x.shape)
        x_zi_shape[axis] = 2
        x_zi_shape = tuple(([n_sections] + x_zi_shape))
        if (zi.shape != x_zi_shape):
            raise ValueError(('Invalid zi shape. With axis=%r, an input with shape %r, and an sos array with %d sections, zi must have shape %r, got %r.' % (axis, x.shape, n_sections, x_zi_shape, zi.shape)))
        zf = np.zeros_like(zi)
    for section in range(n_sections):
        if use_zi:
            (x, zf[section]) = lfilter(sos[section, :3], sos[section, 3:], x, axis, zi=zi[section])
        else:
            x = lfilter(sos[section, :3], sos[section, 3:], x, axis)
    out = ((x, zf) if use_zi else x)
    return out