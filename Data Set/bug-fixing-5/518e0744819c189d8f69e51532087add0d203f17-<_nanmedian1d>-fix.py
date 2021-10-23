def _nanmedian1d(arr1d, overwrite_input=False):
    '\n    Private function for rank 1 arrays. Compute the median ignoring NaNs.\n    See nanmedian for parameter usage\n    '
    (arr1d, overwrite_input) = _remove_nan_1d(arr1d, overwrite_input=overwrite_input)
    if (arr1d.size == 0):
        return np.nan
    return np.median(arr1d, overwrite_input=overwrite_input)