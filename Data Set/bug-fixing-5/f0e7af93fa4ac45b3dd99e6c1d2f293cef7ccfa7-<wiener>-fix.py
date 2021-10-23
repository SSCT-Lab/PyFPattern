def wiener(im, mysize=None, noise=None):
    '\n    Perform a Wiener filter on an N-dimensional array.\n\n    Apply a Wiener filter to the N-dimensional array `im`.\n\n    Parameters\n    ----------\n    im : ndarray\n        An N-dimensional array.\n    mysize : int or array_like, optional\n        A scalar or an N-length list giving the size of the Wiener filter\n        window in each dimension.  Elements of mysize should be odd.\n        If mysize is a scalar, then this scalar is used as the size\n        in each dimension.\n    noise : float, optional\n        The noise-power to use. If None, then noise is estimated as the\n        average of the local variance of the input.\n\n    Returns\n    -------\n    out : ndarray\n        Wiener filtered result with the same shape as `im`.\n\n    '
    im = np.asarray(im)
    if (mysize is None):
        mysize = ([3] * im.ndim)
    mysize = np.asarray(mysize)
    if (mysize.shape == ()):
        mysize = np.repeat(mysize.item(), im.ndim)
    lMean = (correlate(im, np.ones(mysize), 'same') / np.prod(mysize, axis=0))
    lVar = ((correlate((im ** 2), np.ones(mysize), 'same') / np.prod(mysize, axis=0)) - (lMean ** 2))
    if (noise is None):
        noise = np.mean(np.ravel(lVar), axis=0)
    res = (im - lMean)
    res *= (1 - (noise / lVar))
    res += lMean
    out = np.where((lVar < noise), lMean, res)
    return out