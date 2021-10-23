def argsort(x, topn=None, reverse=False):
    'Get indices of the `topn` smallest elements in array `x`.\n\n    Parameters\n    ----------\n    x : array_like\n        Array to sort.\n    topn : int, optional\n        Number of indices of the smallest(greatest) elements to be returned if given,\n        otherwise - indices of all elements will be returned in ascending(descending) order.\n    reverse : bool, optional\n        If True - return the `topn` greatest elements, in descending order.\n\n    Returns\n    -------\n    numpy.ndarray\n        Array of `topn` indices that.sort the array in the required order.\n\n    '
    x = np.asarray(x)
    if (topn is None):
        topn = x.size
    if (topn <= 0):
        return []
    if reverse:
        x = (- x)
    if ((topn >= x.size) or (not hasattr(np, 'argpartition'))):
        return np.argsort(x)[:topn]
    most_extreme = np.argpartition(x, topn)[:topn]
    return most_extreme.take(np.argsort(x.take(most_extreme)))