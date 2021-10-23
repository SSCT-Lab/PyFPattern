def firwin(numtaps, cutoff, width=None, window='hamming', pass_zero=True, scale=True, nyq=None, fs=None):
    '\n    FIR filter design using the window method.\n\n    This function computes the coefficients of a finite impulse response\n    filter.  The filter will have linear phase; it will be Type I if\n    `numtaps` is odd and Type II if `numtaps` is even.\n\n    Type II filters always have zero response at the Nyquist frequency, so a\n    ValueError exception is raised if firwin is called with `numtaps` even and\n    having a passband whose right end is at the Nyquist frequency.\n\n    Parameters\n    ----------\n    numtaps : int\n        Length of the filter (number of coefficients, i.e. the filter\n        order + 1).  `numtaps` must be odd if a passband includes the\n        Nyquist frequency.\n    cutoff : float or 1D array_like\n        Cutoff frequency of filter (expressed in the same units as `nyq`)\n        OR an array of cutoff frequencies (that is, band edges). In the\n        latter case, the frequencies in `cutoff` should be positive and\n        monotonically increasing between 0 and `nyq`.  The values 0 and\n        `nyq` must not be included in `cutoff`.\n    width : float or None, optional\n        If `width` is not None, then assume it is the approximate width\n        of the transition region (expressed in the same units as `nyq`)\n        for use in Kaiser FIR filter design.  In this case, the `window`\n        argument is ignored.\n    window : string or tuple of string and parameter values, optional\n        Desired window to use. See `scipy.signal.get_window` for a list\n        of windows and required parameters.\n    pass_zero : bool, optional\n        If True, the gain at the frequency 0 (i.e. the "DC gain") is 1.\n        Otherwise the DC gain is 0.\n    scale : bool, optional\n        Set to True to scale the coefficients so that the frequency\n        response is exactly unity at a certain frequency.\n        That frequency is either:\n\n        - 0 (DC) if the first passband starts at 0 (i.e. pass_zero\n          is True)\n        - `nyq` (the Nyquist frequency) if the first passband ends at\n          `nyq` (i.e the filter is a single band highpass filter);\n          center of first passband otherwise\n\n    nyq : float, optional\n        *Deprecated.  Use `fs` instead.*  This is the Nyquist frequency.\n        Each frequency in `cutoff` must be between 0 and `nyq`. Default\n        is 1.\n    fs : float, optional\n        The sampling frequency of the signal.  Each frequency in `cutoff`\n        must be between 0 and ``fs/2``.  Default is 2.\n\n    Returns\n    -------\n    h : (numtaps,) ndarray\n        Coefficients of length `numtaps` FIR filter.\n\n    Raises\n    ------\n    ValueError\n        If any value in `cutoff` is less than or equal to 0 or greater\n        than or equal to ``fs/2``, if the values in `cutoff` are not strictly\n        monotonically increasing, or if `numtaps` is even but a passband\n        includes the Nyquist frequency.\n\n    See Also\n    --------\n    firwin2\n    firls\n    minimum_phase\n    remez\n\n    Examples\n    --------\n    Low-pass from 0 to f:\n\n    >>> from scipy import signal\n    >>> numtaps = 3\n    >>> f = 0.1\n    >>> signal.firwin(numtaps, f)\n    array([ 0.06799017,  0.86401967,  0.06799017])\n\n    Use a specific window function:\n\n    >>> signal.firwin(numtaps, f, window=\'nuttall\')\n    array([  3.56607041e-04,   9.99286786e-01,   3.56607041e-04])\n\n    High-pass (\'stop\' from 0 to f):\n\n    >>> signal.firwin(numtaps, f, pass_zero=False)\n    array([-0.00859313,  0.98281375, -0.00859313])\n\n    Band-pass:\n\n    >>> f1, f2 = 0.1, 0.2\n    >>> signal.firwin(numtaps, [f1, f2], pass_zero=False)\n    array([ 0.06301614,  0.88770441,  0.06301614])\n\n    Band-stop:\n\n    >>> signal.firwin(numtaps, [f1, f2])\n    array([-0.00801395,  1.0160279 , -0.00801395])\n\n    Multi-band (passbands are [0, f1], [f2, f3] and [f4, 1]):\n\n    >>> f3, f4 = 0.3, 0.4\n    >>> signal.firwin(numtaps, [f1, f2, f3, f4])\n    array([-0.01376344,  1.02752689, -0.01376344])\n\n    Multi-band (passbands are [f1, f2] and [f3,f4]):\n\n    >>> signal.firwin(numtaps, [f1, f2, f3, f4], pass_zero=False)\n    array([ 0.04890915,  0.91284326,  0.04890915])\n\n    '
    nyq = (0.5 * _get_fs(fs, nyq))
    cutoff = (np.atleast_1d(cutoff) / float(nyq))
    if (cutoff.ndim > 1):
        raise ValueError('The cutoff argument must be at most one-dimensional.')
    if (cutoff.size == 0):
        raise ValueError('At least one cutoff frequency must be given.')
    if ((cutoff.min() <= 0) or (cutoff.max() >= 1)):
        raise ValueError('Invalid cutoff frequency: frequencies must be greater than 0 and less than fs/2.')
    if np.any((np.diff(cutoff) <= 0)):
        raise ValueError('Invalid cutoff frequencies: the frequencies must be strictly increasing.')
    if (width is not None):
        atten = kaiser_atten(numtaps, (float(width) / nyq))
        beta = kaiser_beta(atten)
        window = ('kaiser', beta)
    pass_nyquist = (bool((cutoff.size & 1)) ^ pass_zero)
    if (pass_nyquist and ((numtaps % 2) == 0)):
        raise ValueError('A filter with an even number of coefficients must have zero response at the Nyquist frequency.')
    cutoff = np.hstack((([0.0] * pass_zero), cutoff, ([1.0] * pass_nyquist)))
    bands = cutoff.reshape((- 1), 2)
    alpha = (0.5 * (numtaps - 1))
    m = (np.arange(0, numtaps) - alpha)
    h = 0
    for (left, right) in bands:
        h += (right * sinc((right * m)))
        h -= (left * sinc((left * m)))
    from .signaltools import get_window
    win = get_window(window, numtaps, fftbins=False)
    h *= win
    if scale:
        (left, right) = bands[0]
        if (left == 0):
            scale_frequency = 0.0
        elif (right == 1):
            scale_frequency = 1.0
        else:
            scale_frequency = (0.5 * (left + right))
        c = np.cos(((np.pi * m) * scale_frequency))
        s = np.sum((h * c))
        h /= s
    return h