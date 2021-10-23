def _nanpercentile1d(arr1d, q, overwrite_input=False, interpolation='linear'):
    '\n    Private function for rank 1 arrays. Compute percentile ignoring NaNs.\n    See nanpercentile for parameter usage\n    '
    (arr1d, overwrite_input) = _remove_nan_1d(arr1d, overwrite_input=overwrite_input)
    if (arr1d.size == 0):
        return np.full(q.shape, np.nan)[()]
    return np.percentile(arr1d, q, overwrite_input=overwrite_input, interpolation=interpolation)