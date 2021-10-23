def _nanmedian1d(arr1d, overwrite_input=False):
    '\n    Private function for rank 1 arrays. Compute the median ignoring NaNs.\n    See nanmedian for parameter usage\n    '
    c = np.isnan(arr1d)
    s = np.nonzero(c)[0]
    if (s.size == arr1d.size):
        warnings.warn('All-NaN slice encountered', RuntimeWarning, stacklevel=3)
        return np.nan
    elif (s.size == 0):
        return np.median(arr1d, overwrite_input=overwrite_input)
    else:
        if overwrite_input:
            x = arr1d
        else:
            x = arr1d.copy()
        enonan = arr1d[(- s.size):][(~ c[(- s.size):])]
        x[s[:enonan.size]] = enonan
        return np.median(x[:(- s.size)], overwrite_input=True)