def iirfilter(N, Wn, rp=None, rs=None, btype='band', analog=False, ftype='butter', output='ba', fs=None):
    "\n    IIR digital and analog filter design given order and critical points.\n\n    Design an Nth-order digital or analog filter and return the filter\n    coefficients.\n\n    Parameters\n    ----------\n    N : int\n        The order of the filter.\n    Wn : array_like\n        A scalar or length-2 sequence giving the critical frequencies.\n\n        For digital filters, `Wn` are in the same units as `fs`. By default,\n        `fs` is 2 half-cycles/sample, so these are normalized from 0 to 1,\n        where 1 is the Nyquist frequency. (`Wn` is thus in\n        half-cycles / sample.)\n\n        For analog filters, `Wn` is an angular frequency (e.g., rad/s).\n    rp : float, optional\n        For Chebyshev and elliptic filters, provides the maximum ripple\n        in the passband. (dB)\n    rs : float, optional\n        For Chebyshev and elliptic filters, provides the minimum attenuation\n        in the stop band. (dB)\n    btype : {'bandpass', 'lowpass', 'highpass', 'bandstop'}, optional\n        The type of filter.  Default is 'bandpass'.\n    analog : bool, optional\n        When True, return an analog filter, otherwise a digital filter is\n        returned.\n    ftype : str, optional\n        The type of IIR filter to design:\n\n            - Butterworth   : 'butter'\n            - Chebyshev I   : 'cheby1'\n            - Chebyshev II  : 'cheby2'\n            - Cauer/elliptic: 'ellip'\n            - Bessel/Thomson: 'bessel'\n\n    output : {'ba', 'zpk', 'sos'}, optional\n        Type of output:  numerator/denominator ('ba'), pole-zero ('zpk'), or\n        second-order sections ('sos'). Default is 'ba' for backwards\n        compatibility, but 'sos' should be used for general-purpose filtering.\n    fs : float, optional\n        The sampling frequency of the digital system.\n\n        .. versionadded:: 1.2.0\n\n    Returns\n    -------\n    b, a : ndarray, ndarray\n        Numerator (`b`) and denominator (`a`) polynomials of the IIR filter.\n        Only returned if ``output='ba'``.\n    z, p, k : ndarray, ndarray, float\n        Zeros, poles, and system gain of the IIR filter transfer\n        function.  Only returned if ``output='zpk'``.\n    sos : ndarray\n        Second-order sections representation of the IIR filter.\n        Only returned if ``output=='sos'``.\n\n    See Also\n    --------\n    butter : Filter design using order and critical points\n    cheby1, cheby2, ellip, bessel\n    buttord : Find order and critical points from passband and stopband spec\n    cheb1ord, cheb2ord, ellipord\n    iirdesign : General filter design using passband and stopband spec\n\n    Notes\n    -----\n    The ``'sos'`` output parameter was added in 0.16.0.\n\n    Examples\n    --------\n    Generate a 17th-order Chebyshev II analog bandpass filter from 50 Hz to\n    200 Hz and plot the frequency response:\n\n    >>> from scipy import signal\n    >>> import matplotlib.pyplot as plt\n\n    >>> b, a = signal.iirfilter(17, [2*np.pi*50, 2*np.pi*200], rs=60,\n    ...                         btype='band', analog=True, ftype='cheby2')\n    >>> w, h = signal.freqs(b, a, 1000)\n    >>> fig = plt.figure()\n    >>> ax = fig.add_subplot(1, 1, 1)\n    >>> ax.semilogx(w / (2*np.pi), 20 * np.log10(np.maximum(abs(h), 1e-5)))\n    >>> ax.set_title('Chebyshev Type II bandpass frequency response')\n    >>> ax.set_xlabel('Frequency [Hz]')\n    >>> ax.set_ylabel('Amplitude [dB]')\n    >>> ax.axis((10, 1000, -100, 10))\n    >>> ax.grid(which='both', axis='both')\n    >>> plt.show()\n\n    Create a digital filter with the same properties, in a system with\n    sampling rate of 2000 Hz, and plot the frequency response. (Second-order\n    sections implementation is required to ensure stability of a filter of\n    this order):\n\n    >>> sos = signal.iirfilter(17, [50, 200], rs=60, btype='band',\n    ...                        analog=False, ftype='cheby2', fs=2000,\n    ...                        output='sos')\n    >>> w, h = signal.sosfreqz(sos, 2000, fs=2000)\n    >>> fig = plt.figure()\n    >>> ax = fig.add_subplot(1, 1, 1)\n    >>> ax.semilogx(w, 20 * np.log10(np.maximum(abs(h), 1e-5)))\n    >>> ax.set_title('Chebyshev Type II bandpass frequency response')\n    >>> ax.set_xlabel('Frequency [Hz]')\n    >>> ax.set_ylabel('Amplitude [dB]')\n    >>> ax.axis((10, 1000, -100, 10))\n    >>> ax.grid(which='both', axis='both')\n    >>> plt.show()\n\n    "
    (ftype, btype, output) = [x.lower() for x in (ftype, btype, output)]
    Wn = asarray(Wn)
    if (fs is not None):
        if analog:
            raise ValueError('fs cannot be specified for an analog filter')
        Wn = ((2 * Wn) / fs)
    try:
        btype = band_dict[btype]
    except KeyError:
        raise ValueError(("'%s' is an invalid bandtype for filter." % btype))
    try:
        typefunc = filter_dict[ftype][0]
    except KeyError:
        raise ValueError(("'%s' is not a valid basic IIR filter." % ftype))
    if (output not in ['ba', 'zpk', 'sos']):
        raise ValueError(("'%s' is not a valid output form." % output))
    if ((rp is not None) and (rp < 0)):
        raise ValueError('passband ripple (rp) must be positive')
    if ((rs is not None) and (rs < 0)):
        raise ValueError('stopband attenuation (rs) must be positive')
    if (typefunc == buttap):
        (z, p, k) = typefunc(N)
    elif (typefunc == besselap):
        (z, p, k) = typefunc(N, norm=bessel_norms[ftype])
    elif (typefunc == cheb1ap):
        if (rp is None):
            raise ValueError('passband ripple (rp) must be provided to design a Chebyshev I filter.')
        (z, p, k) = typefunc(N, rp)
    elif (typefunc == cheb2ap):
        if (rs is None):
            raise ValueError('stopband attenuation (rs) must be provided to design an Chebyshev II filter.')
        (z, p, k) = typefunc(N, rs)
    elif (typefunc == ellipap):
        if ((rs is None) or (rp is None)):
            raise ValueError('Both rp and rs must be provided to design an elliptic filter.')
        (z, p, k) = typefunc(N, rp, rs)
    else:
        raise NotImplementedError(("'%s' not implemented in iirfilter." % ftype))
    if (not analog):
        if (numpy.any((Wn <= 0)) or numpy.any((Wn >= 1))):
            if (fs is not None):
                raise ValueError('Digital filter critical frequencies must be 0 < Wn < fs/2 (fs={} -> fs/2={})'.format(fs, (fs / 2)))
            raise ValueError('Digital filter critical frequencies must be 0 < Wn < 1')
        fs = 2.0
        warped = ((2 * fs) * tan(((pi * Wn) / fs)))
    else:
        warped = Wn
    if (btype in ('lowpass', 'highpass')):
        if (numpy.size(Wn) != 1):
            raise ValueError('Must specify a single critical frequency Wn for lowpass or highpass filter')
        if (btype == 'lowpass'):
            (z, p, k) = lp2lp_zpk(z, p, k, wo=warped)
        elif (btype == 'highpass'):
            (z, p, k) = lp2hp_zpk(z, p, k, wo=warped)
    elif (btype in ('bandpass', 'bandstop')):
        try:
            bw = (warped[1] - warped[0])
            wo = sqrt((warped[0] * warped[1]))
        except IndexError:
            raise ValueError('Wn must specify start and stop frequencies for bandpass or bandstop filter')
        if (btype == 'bandpass'):
            (z, p, k) = lp2bp_zpk(z, p, k, wo=wo, bw=bw)
        elif (btype == 'bandstop'):
            (z, p, k) = lp2bs_zpk(z, p, k, wo=wo, bw=bw)
    else:
        raise NotImplementedError(("'%s' not implemented in iirfilter." % btype))
    if (not analog):
        (z, p, k) = bilinear_zpk(z, p, k, fs=fs)
    if (output == 'zpk'):
        return (z, p, k)
    elif (output == 'ba'):
        return zpk2tf(z, p, k)
    elif (output == 'sos'):
        return zpk2sos(z, p, k)