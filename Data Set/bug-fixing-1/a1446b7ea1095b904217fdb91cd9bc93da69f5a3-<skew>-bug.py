

def skew(a, axis=0, bias=True, nan_policy='propagate'):
    "\n    Compute the skewness of a data set.\n\n    For normally distributed data, the skewness should be about 0. A skewness\n    value > 0 means that there is more weight in the left tail of the\n    distribution. The function `skewtest` can be used to determine if the\n    skewness value is close enough to 0, statistically speaking.\n\n    Parameters\n    ----------\n    a : ndarray\n        data\n    axis : int or None, optional\n        Axis along which skewness is calculated. Default is 0.\n        If None, compute over the whole array `a`.\n    bias : bool, optional\n        If False, then the calculations are corrected for statistical bias.\n    nan_policy : {'propagate', 'raise', 'omit'}, optional\n        Defines how to handle when input contains nan. 'propagate' returns nan,\n        'raise' throws an error, 'omit' performs the calculations ignoring nan\n        values. Default is 'propagate'.\n\n    Returns\n    -------\n    skewness : ndarray\n        The skewness of values along an axis, returning 0 where all values are\n        equal.\n\n    References\n    ----------\n\n    .. [1] Zwillinger, D. and Kokoska, S. (2000). CRC Standard\n       Probability and Statistics Tables and Formulae. Chapman & Hall: New\n       York. 2000.\n       Section 2.2.24.1\n\n    Examples\n    --------\n    >>> from scipy.stats import skew\n    >>> skew([1, 2, 3, 4, 5])\n    0.0\n    >>> skew([2, 8, 0, 4, 1, 9, 9, 0])\n    0.2650554122698573\n    "
    (a, axis) = _chk_asarray(a, axis)
    n = a.shape[axis]
    (contains_nan, nan_policy) = _contains_nan(a, nan_policy)
    if (contains_nan and (nan_policy == 'omit')):
        a = ma.masked_invalid(a)
        return mstats_basic.skew(a, axis, bias)
    m2 = moment(a, 2, axis)
    m3 = moment(a, 3, axis)
    zero = (m2 == 0)
    vals = _lazywhere((~ zero), (m2, m3), (lambda m2, m3: (m3 / (m2 ** 1.5))), 0.0)
    if (not bias):
        can_correct = ((n > 2) & (m2 > 0))
        if can_correct.any():
            m2 = np.extract(can_correct, m2)
            m3 = np.extract(can_correct, m3)
            nval = (((np.sqrt(((n - 1.0) * n)) / (n - 2.0)) * m3) / (m2 ** 1.5))
            np.place(vals, can_correct, nval)
    if (vals.ndim == 0):
        return vals.item()
    return vals
