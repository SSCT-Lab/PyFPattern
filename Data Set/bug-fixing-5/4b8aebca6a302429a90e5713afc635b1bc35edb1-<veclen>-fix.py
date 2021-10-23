def veclen(vec):
    'Calculate length of vector\n\n    Parameters\n    ----------\n    vec : list of (int, number)\n        Input vector in BoW format.\n\n    Returns\n    -------\n    float\n        Length of `vec`.\n\n    '
    if (len(vec) == 0):
        return 0.0
    length = (1.0 * math.sqrt(sum(((val ** 2) for (_, val) in vec))))
    assert (length > 0.0), 'sparse documents must not contain any explicit zero entries'
    return length