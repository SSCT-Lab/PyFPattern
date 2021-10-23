def ricker(points, a):
    '\n    Return a Ricker wavelet, also known as the "Mexican hat wavelet".\n\n    It models the function:\n\n        ``A (1 - x^2/a^2) exp(-x^2/2 a^2)``,\n\n    where ``A = 2/sqrt(3a)pi^1/4``.\n\n    Parameters\n    ----------\n    points : int\n        Number of points in `vector`.\n        Will be centered around 0.\n    a : scalar\n        Width parameter of the wavelet.\n\n    Returns\n    -------\n    vector : (N,) ndarray\n        Array of length `points` in shape of ricker curve.\n\n    Examples\n    --------\n    >>> from scipy import signal\n    >>> import matplotlib.pyplot as plt\n\n    >>> points = 100\n    >>> a = 4.0\n    >>> vec2 = signal.ricker(points, a)\n    >>> print(len(vec2))\n    100\n    >>> plt.plot(vec2)\n    >>> plt.show()\n\n    '
    A = (2 / (np.sqrt((3 * a)) * (np.pi ** 0.25)))
    wsq = (a ** 2)
    vec = (np.arange(0, points) - ((points - 1.0) / 2))
    xsq = (vec ** 2)
    mod = (1 - (xsq / wsq))
    gauss = np.exp(((- xsq) / (2 * wsq)))
    total = ((A * mod) * gauss)
    return total