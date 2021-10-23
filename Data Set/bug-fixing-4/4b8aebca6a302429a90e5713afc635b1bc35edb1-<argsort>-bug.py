def argsort(x, topn=None, reverse=False):
    '\n    Return indices of the `topn` smallest elements in array `x`, in ascending order.\n\n    If reverse is True, return the greatest elements instead, in descending order.\n\n    '
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