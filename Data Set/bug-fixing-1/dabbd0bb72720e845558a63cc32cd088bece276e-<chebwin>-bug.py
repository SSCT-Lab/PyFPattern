

def chebwin(M, at, sym=True):
    'Return a Dolph-Chebyshev window.\n\n    Parameters\n    ----------\n    M : int\n        Number of points in the output window. If zero or less, an empty\n        array is returned.\n    at : float\n        Attenuation (in dB).\n    sym : bool, optional\n        When True (default), generates a symmetric window, for use in filter\n        design.\n        When False, generates a periodic window, for use in spectral analysis.\n\n    Returns\n    -------\n    w : ndarray\n        The window, with the maximum value always normalized to 1\n\n    Notes\n    -----\n    This window optimizes for the narrowest main lobe width for a given order\n    `M` and sidelobe equiripple attenuation `at`, using Chebyshev\n    polynomials.  It was originally developed by Dolph to optimize the\n    directionality of radio antenna arrays.\n\n    Unlike most windows, the Dolph-Chebyshev is defined in terms of its\n    frequency response:\n\n    .. math:: W(k) = \\frac\n              {\\cos\\{M \\cos^{-1}[\\beta \\cos(\\frac{\\pi k}{M})]\\}}\n              {\\cosh[M \\cosh^{-1}(\\beta)]}\n\n    where\n\n    .. math:: \\beta = \\cosh \\left [\\frac{1}{M}\n              \\cosh^{-1}(10^\\frac{A}{20}) \\right ]\n\n    and 0 <= abs(k) <= M-1. A is the attenuation in decibels (`at`).\n\n    The time domain window is then generated using the IFFT, so\n    power-of-two `M` are the fastest to generate, and prime number `M` are\n    the slowest.\n\n    The equiripple condition in the frequency domain creates impulses in the\n    time domain, which appear at the ends of the window.\n\n    References\n    ----------\n    .. [1] C. Dolph, "A current distribution for broadside arrays which\n           optimizes the relationship between beam width and side-lobe level",\n           Proceedings of the IEEE, Vol. 34, Issue 6\n    .. [2] Peter Lynch, "The Dolph-Chebyshev Window: A Simple Optimal Filter",\n           American Meteorological Society (April 1997)\n           http://mathsci.ucd.ie/~plynch/Publications/Dolph.pdf\n    .. [3] F. J. Harris, "On the use of windows for harmonic analysis with the\n           discrete Fourier transforms", Proceedings of the IEEE, Vol. 66,\n           No. 1, January 1978\n\n    Examples\n    --------\n    Plot the window and its frequency response:\n\n    >>> from scipy import signal\n    >>> from scipy.fftpack import fft, fftshift\n    >>> import matplotlib.pyplot as plt\n\n    >>> window = signal.chebwin(51, at=100)\n    >>> plt.plot(window)\n    >>> plt.title("Dolph-Chebyshev window (100 dB)")\n    >>> plt.ylabel("Amplitude")\n    >>> plt.xlabel("Sample")\n\n    >>> plt.figure()\n    >>> A = fft(window, 2048) / (len(window)/2.0)\n    >>> freq = np.linspace(-0.5, 0.5, len(A))\n    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))\n    >>> plt.plot(freq, response)\n    >>> plt.axis([-0.5, 0.5, -120, 0])\n    >>> plt.title("Frequency response of the Dolph-Chebyshev window (100 dB)")\n    >>> plt.ylabel("Normalized magnitude [dB]")\n    >>> plt.xlabel("Normalized frequency [cycles per sample]")\n\n    '
    if (np.abs(at) < 45):
        warnings.warn('This window is not suitable for spectral analysis for attenuation values lower than about 45dB because the equivalent noise bandwidth of a Chebyshev window does not grow monotonically with increasing sidelobe attenuation when the attenuation is smaller than about 45 dB.')
    if _len_guards(M):
        return np.ones(M)
    (M, needs_trunc) = _extend(M, sym)
    order = (M - 1.0)
    beta = np.cosh(((1.0 / order) * np.arccosh((10 ** (np.abs(at) / 20.0)))))
    k = (np.r_[0:M] * 1.0)
    x = (beta * np.cos(((np.pi * k) / M)))
    p = np.zeros(x.shape)
    p[(x > 1)] = np.cosh((order * np.arccosh(x[(x > 1)])))
    p[(x < (- 1))] = ((1 - (2 * (order % 2))) * np.cosh((order * np.arccosh((- x[(x < (- 1))])))))
    p[(np.abs(x) <= 1)] = np.cos((order * np.arccos(x[(np.abs(x) <= 1)])))
    if (M % 2):
        w = np.real(fftpack.fft(p))
        n = ((M + 1) // 2)
        w = w[:n]
        w = np.concatenate((w[(n - 1):0:(- 1)], w))
    else:
        p = (p * np.exp((((1j * np.pi) / M) * np.r_[0:M])))
        w = np.real(fftpack.fft(p))
        n = ((M // 2) + 1)
        w = np.concatenate((w[(n - 1):0:(- 1)], w[1:n]))
    w = (w / max(w))
    return _truncate(w, needs_trunc)
