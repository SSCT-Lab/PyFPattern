def reldiff(a, b):
    'Calculate the relative difference between two input arrays\n\n    Calculated by :math:`\\frac{|a-b|_1}{|a|_1 + |b|_1}`\n\n    Parameters\n    ----------\n    a : np.ndarray\n    b : np.ndarray\n    '
    diff = np.sum(np.abs((a - b)))
    norm = (np.sum(np.abs(a)) + np.sum(np.abs(b)))
    if (diff == 0):
        return 0
    ret = (diff / norm)
    return ret