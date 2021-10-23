def butter(N, Wn, btype='low', analog=False, output='ba', fs=None):
    '\n    Butterworth digital and analog filter design.\n\n    Design an Nth-order digital or analog Butterworth filter and return\n    the filter coefficients.\n\n    Parameters\n    ----------\n    N : int\n        The order of the filter.\n    Wn : array_like\n        The critical frequency or frequencies. For lowpass and highpass\n        filters, Wn is a scalar; for bandpass and bandstop filters,\n        Wn is a length-2 sequence.\n\n        For a Butterworth filter, this is the point at which the gain\n        drops to 1/sqrt(2) that of the passband (the "-3 dB point").\n\n        For digital filters, `Wn` are in the same units as `fs`.  By default,\n        `fs` is 2 half-cycles/sample, so these are normalized from 0 to 1,\n        where 1 is the Nyquist frequency.  (`Wn` is thus in\n        half-cycles / sample.)\n\n        For analog filters, `Wn` is an angular frequency (e.g. rad/s).\n    btype : {\'lowpass\', \'highpass\', \'bandpass\', \'bandstop\'}, optional\n        The type of filter.  Default is \'lowpass\'.\n    analog : bool, optional\n        When True, return an analog filter, otherwise a digital filter is\n        returned.\n    output : {\'ba\', \'zpk\', \'sos\'}, optional\n        Type of output:  numerator/denominator (\'ba\'), pole-zero (\'zpk\'), or\n        second-order sections (\'sos\'). Default is \'ba\' for backwards\n        compatibility, but \'sos\' should be used for general-purpose filtering.\n    fs : float, optional\n        The sampling frequency of the digital system.\n\n        .. versionadded:: 1.2.0\n\n    Returns\n    -------\n    b, a : ndarray, ndarray\n        Numerator (`b`) and denominator (`a`) polynomials of the IIR filter.\n        Only returned if ``output=\'ba\'``.\n    z, p, k : ndarray, ndarray, float\n        Zeros, poles, and system gain of the IIR filter transfer\n        function.  Only returned if ``output=\'zpk\'``.\n    sos : ndarray\n        Second-order sections representation of the IIR filter.\n        Only returned if ``output==\'sos\'``.\n\n    See Also\n    --------\n    buttord, buttap\n\n    Notes\n    -----\n    The Butterworth filter has maximally flat frequency response in the\n    passband.\n\n    The ``\'sos\'`` output parameter was added in 0.16.0.\n\n    Examples\n    --------\n    Design an analog filter and plot its frequency response, showing the\n    critical points:\n\n    >>> from scipy import signal\n    >>> import matplotlib.pyplot as plt\n\n    >>> b, a = signal.butter(4, 100, \'low\', analog=True)\n    >>> w, h = signal.freqs(b, a)\n    >>> plt.semilogx(w, 20 * np.log10(abs(h)))\n    >>> plt.title(\'Butterworth filter frequency response\')\n    >>> plt.xlabel(\'Frequency [radians / second]\')\n    >>> plt.ylabel(\'Amplitude [dB]\')\n    >>> plt.margins(0, 0.1)\n    >>> plt.grid(which=\'both\', axis=\'both\')\n    >>> plt.axvline(100, color=\'green\') # cutoff frequency\n    >>> plt.show()\n\n    Generate a signal made up of 10 Hz and 20 Hz, sampled at 1 kHz\n\n    >>> t = np.linspace(0, 1, 1000, False)  # 1 second\n    >>> sig = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*20*t)\n    >>> fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)\n    >>> ax1.plot(t, sig)\n    >>> ax1.set_title(\'10 Hz and 20 Hz sinusoids\')\n    >>> ax1.axis([0, 1, -2, 2])\n\n    Design a digital high-pass filter at 15 Hz to remove the 10 Hz tone, and\n    apply it to the signal.  (It\'s recommended to use second-order sections\n    format when filtering, to avoid numerical error with transfer function\n    (``ba``) format):\n\n    >>> sos = signal.butter(10, 15, \'hp\', fs=1000, output=\'sos\')\n    >>> filtered = signal.sosfilt(sos, sig)\n    >>> ax2.plot(t, filtered)\n    >>> ax2.set_title(\'After 15 Hz high-pass filter\')\n    >>> ax2.axis([0, 1, -2, 2])\n    >>> ax2.set_xlabel(\'Time [seconds]\')\n    >>> plt.tight_layout()\n    >>> plt.show()\n    '
    return iirfilter(N, Wn, btype=btype, analog=analog, output=output, ftype='butter', fs=fs)