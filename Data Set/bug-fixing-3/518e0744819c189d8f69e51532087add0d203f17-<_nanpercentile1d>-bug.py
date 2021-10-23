def _nanpercentile1d(arr1d, q, overwrite_input=False, interpolation='linear'):
    '\n    Private function for rank 1 arrays. Compute percentile ignoring\n    NaNs.\n\n    See nanpercentile for parameter usage\n    '
    c = np.isnan(arr1d)
    s = np.nonzero(c)[0]
    if (s.size == arr1d.size):
        warnings.warn('All-NaN slice encountered', RuntimeWarning, stacklevel=3)
        if (q.ndim == 0):
            return np.nan
        else:
            return (np.nan * np.ones((len(q),)))
    elif (s.size == 0):
        return np.percentile(arr1d, q, overwrite_input=overwrite_input, interpolation=interpolation)
    else:
        if overwrite_input:
            x = arr1d
        else:
            x = arr1d.copy()
        enonan = arr1d[(- s.size):][(~ c[(- s.size):])]
        x[s[:enonan.size]] = enonan
        return np.percentile(x[:(- s.size)], q, overwrite_input=True, interpolation=interpolation)