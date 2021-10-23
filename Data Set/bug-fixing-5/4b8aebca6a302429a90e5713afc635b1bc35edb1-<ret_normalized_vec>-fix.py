def ret_normalized_vec(vec, length):
    'Normalize vector.\n\n    Parameters\n    ----------\n    vec : list of (int, number)\n        Input vector in BoW format.\n    length : float\n        Length of vector\n\n    Returns\n    -------\n    list of (int, number)\n        Normalized vector in BoW format.\n\n    '
    if (length != 1.0):
        return [(termid, (val / length)) for (termid, val) in vec]
    else:
        return list(vec)