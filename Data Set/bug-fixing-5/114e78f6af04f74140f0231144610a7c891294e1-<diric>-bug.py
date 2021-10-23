def diric(x, n):
    "Periodic sinc function, also called the Dirichlet function.\n\n    The Dirichlet function is defined as::\n\n        diric(x) = sin(x * n/2) / (n * sin(x / 2)),\n\n    where `n` is a positive integer.\n\n    Parameters\n    ----------\n    x : array_like\n        Input data\n    n : int\n        Integer defining the periodicity.\n\n    Returns\n    -------\n    diric : ndarray\n\n    Examples\n    --------\n    >>> from scipy import special\n    >>> import matplotlib.pyplot as plt\n\n    >>> x = np.linspace(-8*np.pi, 8*np.pi, num=201)\n    >>> plt.figure(figsize=(8, 8));\n    >>> for idx, n in enumerate([2, 3, 4, 9]):\n    ...     plt.subplot(2, 2, idx+1)\n    ...     plt.plot(x, special.diric(x, n))\n    ...     plt.title('diric, n={}'.format(n))\n    >>> plt.show()\n\n    The following example demonstrates that `diric` gives the magnitudes\n    (modulo the sign and scaling) of the Fourier coefficients of a\n    rectangular pulse.\n\n    Suppress output of values that are effectively 0:\n\n    >>> np.set_printoptions(suppress=True)\n\n    Create a signal `x` of length `m` with `k` ones:\n\n    >>> m = 8\n    >>> k = 3\n    >>> x = np.zeros(m)\n    >>> x[:k] = 1\n\n    Use the FFT to compute the Fourier transform of `x`, and\n    inspect the magnitudes of the coefficients:\n\n    >>> np.abs(np.fft.fft(x))\n    array([ 3.        ,  2.41421356,  1.        ,  0.41421356,  1.        ,\n            0.41421356,  1.        ,  2.41421356])\n\n    Now find the same values (up to sign) using `diric`.  We multiply\n    by `k` to account for the different scaling conventions of\n    `numpy.fft.fft` and `diric`:\n\n    >>> theta = np.linspace(0, 2*np.pi, m, endpoint=False)\n    >>> k * special.diric(theta, k)\n    array([ 3.        ,  2.41421356,  1.        , -0.41421356, -1.        ,\n           -0.41421356,  1.        ,  2.41421356])\n    "
    (x, n) = (asarray(x), asarray(n))
    n = asarray((n + (x - x)))
    x = asarray((x + (n - n)))
    if issubdtype(x.dtype, inexact):
        ytype = x.dtype
    else:
        ytype = float
    y = zeros(x.shape, ytype)
    if (np.finfo(ytype).eps < 1e-18):
        minval = 1e-11
    elif (np.finfo(ytype).eps < 1e-15):
        minval = 1e-07
    else:
        minval = 0.001
    mask1 = ((n <= 0) | (n != floor(n)))
    place(y, mask1, nan)
    x = (x / 2)
    denom = sin(x)
    mask2 = ((1 - mask1) & (abs(denom) < minval))
    xsub = extract(mask2, x)
    nsub = extract(mask2, n)
    zsub = (xsub / pi)
    place(y, mask2, pow((- 1), (np.round(zsub) * (nsub - 1))))
    mask = ((1 - mask1) & (1 - mask2))
    xsub = extract(mask, x)
    nsub = extract(mask, n)
    dsub = extract(mask, denom)
    place(y, mask, (sin((nsub * xsub)) / (nsub * dsub)))
    return y