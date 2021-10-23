@disallow('M8', 'm8')
def nankurt(values, axis=None, skipna=True):
    ' Compute the sample skewness.\n\n    The statistic computed here is the adjusted Fisher-Pearson standardized\n    moment coefficient G2, computed directly from the second and fourth\n    central moment.\n\n    '
    values = _values_from_object(values)
    mask = isna(values)
    if (not is_float_dtype(values.dtype)):
        values = values.astype('f8')
        count = _get_counts(mask, axis)
    else:
        count = _get_counts(mask, axis, dtype=values.dtype)
    if skipna:
        values = values.copy()
        np.putmask(values, mask, 0)
    mean = (values.sum(axis, dtype=np.float64) / count)
    if (axis is not None):
        mean = np.expand_dims(mean, axis)
    adjusted = (values - mean)
    if skipna:
        np.putmask(adjusted, mask, 0)
    adjusted2 = (adjusted ** 2)
    adjusted4 = (adjusted2 ** 2)
    m2 = adjusted2.sum(axis, dtype=np.float64)
    m4 = adjusted4.sum(axis, dtype=np.float64)
    with np.errstate(invalid='ignore', divide='ignore'):
        adj = ((3 * ((count - 1) ** 2)) / ((count - 2) * (count - 3)))
        numer = (((count * (count + 1)) * (count - 1)) * m4)
        denom = (((count - 2) * (count - 3)) * (m2 ** 2))
        result = ((numer / denom) - adj)
    numer = _zero_out_fperr(numer)
    denom = _zero_out_fperr(denom)
    if (not isinstance(denom, np.ndarray)):
        if (count < 4):
            return np.nan
        if (denom == 0):
            return 0
    with np.errstate(invalid='ignore', divide='ignore'):
        result = ((numer / denom) - adj)
    dtype = values.dtype
    if is_float_dtype(dtype):
        result = result.astype(dtype)
    if isinstance(result, np.ndarray):
        result = np.where((denom == 0), 0, result)
        result[(count < 4)] = np.nan
    return result