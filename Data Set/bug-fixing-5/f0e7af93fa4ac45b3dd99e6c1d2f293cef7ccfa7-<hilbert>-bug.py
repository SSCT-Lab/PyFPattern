def hilbert(x, N=None, axis=(- 1)):
    '\n    Compute the analytic signal, using the Hilbert transform.\n\n    The transformation is done along the last axis by default.\n\n    Parameters\n    ----------\n    x : array_like\n        Signal data.  Must be real.\n    N : int, optional\n        Number of Fourier components.  Default: ``x.shape[axis]``\n    axis : int, optional\n        Axis along which to do the transformation.  Default: -1.\n\n    Returns\n    -------\n    xa : ndarray\n        Analytic signal of `x`, of each 1-D array along `axis`\n\n    Notes\n    -----\n    The analytic signal ``x_a(t)`` of signal ``x(t)`` is:\n\n    .. math:: x_a = F^{-1}(F(x) 2U) = x + i y\n\n    where `F` is the Fourier transform, `U` the unit step function,\n    and `y` the Hilbert transform of `x`. [1]_\n\n    In other words, the negative half of the frequency spectrum is zeroed\n    out, turning the real-valued signal into a complex signal.  The Hilbert\n    transformed signal can be obtained from ``np.imag(hilbert(x))``, and the\n    original signal from ``np.real(hilbert(x))``.\n\n    Examples\n    ---------\n    In this example we use the Hilbert transform to determine the amplitude\n    envelope and instantaneous frequency of an amplitude-modulated signal.\n\n    >>> import numpy as np\n    >>> import matplotlib.pyplot as plt\n    >>> from scipy.signal import hilbert, chirp\n\n    >>> duration = 1.0\n    >>> fs = 400.0\n    >>> samples = int(fs*duration)\n    >>> t = np.arange(samples) / fs\n\n    We create a chirp of which the frequency increases from 20 Hz to 100 Hz and\n    apply an amplitude modulation.\n\n    >>> signal = chirp(t, 20.0, t[-1], 100.0)\n    >>> signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t) )\n\n    The amplitude envelope is given by magnitude of the analytic signal. The\n    instantaneous frequency can be obtained by differentiating the\n    instantaneous phase in respect to time. The instantaneous phase corresponds\n    to the phase angle of the analytic signal.\n\n    >>> analytic_signal = hilbert(signal)\n    >>> amplitude_envelope = np.abs(analytic_signal)\n    >>> instantaneous_phase = np.unwrap(np.angle(analytic_signal))\n    >>> instantaneous_frequency = (np.diff(instantaneous_phase) /\n    ...                            (2.0*np.pi) * fs)\n\n    >>> fig = plt.figure()\n    >>> ax0 = fig.add_subplot(211)\n    >>> ax0.plot(t, signal, label=\'signal\')\n    >>> ax0.plot(t, amplitude_envelope, label=\'envelope\')\n    >>> ax0.set_xlabel("time in seconds")\n    >>> ax0.legend()\n    >>> ax1 = fig.add_subplot(212)\n    >>> ax1.plot(t[1:], instantaneous_frequency)\n    >>> ax1.set_xlabel("time in seconds")\n    >>> ax1.set_ylim(0.0, 120.0)\n\n    References\n    ----------\n    .. [1] Wikipedia, "Analytic signal".\n           https://en.wikipedia.org/wiki/Analytic_signal\n    .. [2] Leon Cohen, "Time-Frequency Analysis", 1995. Chapter 2.\n    .. [3] Alan V. Oppenheim, Ronald W. Schafer. Discrete-Time Signal\n           Processing, Third Edition, 2009. Chapter 12.\n           ISBN 13: 978-1292-02572-8\n\n    '
    x = asarray(x)
    if iscomplexobj(x):
        raise ValueError('x must be real.')
    if (N is None):
        N = x.shape[axis]
    if (N <= 0):
        raise ValueError('N must be positive.')
    Xf = sp_fft.fft(x, N, axis=axis)
    h = zeros(N)
    if ((N % 2) == 0):
        h[0] = h[(N // 2)] = 1
        h[1:(N // 2)] = 2
    else:
        h[0] = 1
        h[1:((N + 1) // 2)] = 2
    if (x.ndim > 1):
        ind = ([newaxis] * x.ndim)
        ind[axis] = slice(None)
        h = h[tuple(ind)]
    x = sp_fft.ifft((Xf * h), axis=axis)
    return x