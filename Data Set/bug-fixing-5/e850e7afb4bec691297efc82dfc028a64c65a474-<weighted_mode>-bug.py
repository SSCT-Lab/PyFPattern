def weighted_mode(a, w, axis=0):
    "Returns an array of the weighted modal (most common) value in a\n\n    If there is more than one such value, only the first is returned.\n    The bin-count for the modal bins is also returned.\n\n    This is an extension of the algorithm in scipy.stats.mode.\n\n    Parameters\n    ----------\n    a : array_like\n        n-dimensional array of which to find mode(s).\n    w : array_like\n        n-dimensional array of weights for each value\n    axis : int, optional\n        Axis along which to operate. Default is 0, i.e. the first axis.\n\n    Returns\n    -------\n    vals : ndarray\n        Array of modal values.\n    score : ndarray\n        Array of weighted counts for each mode.\n\n    Examples\n    --------\n    >>> from sklearn.utils.extmath import weighted_mode\n    >>> x = [4, 1, 4, 2, 4, 2]\n    >>> weights = [1, 1, 1, 1, 1, 1]\n    >>> weighted_mode(x, weights)\n    (array([4.]), array([3.]))\n\n    The value 4 appears three times: with uniform weights, the result is\n    simply the mode of the distribution.\n\n    >>> weights = [1, 3, 0.5, 1.5, 1, 2] # deweight the 4's\n    >>> weighted_mode(x, weights)\n    (array([2.]), array([3.5]))\n\n    The value 2 has the highest score: it appears twice with weights of\n    1.5 and 2: the sum of these is 3.\n\n    See Also\n    --------\n    scipy.stats.mode\n    "
    if (axis is None):
        a = np.ravel(a)
        w = np.ravel(w)
        axis = 0
    else:
        a = np.asarray(a)
        w = np.asarray(w)
    if (a.shape != w.shape):
        w = np.full(a.shape, w, dtype=w.dtype)
    scores = np.unique(np.ravel(a))
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)
    for score in scores:
        template = np.zeros(a.shape)
        ind = (a == score)
        template[ind] = w[ind]
        counts = np.expand_dims(np.sum(template, axis), axis)
        mostfrequent = np.where((counts > oldcounts), score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent
    return (mostfrequent, oldcounts)