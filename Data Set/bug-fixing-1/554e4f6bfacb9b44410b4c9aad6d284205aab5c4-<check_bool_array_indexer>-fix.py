

def check_bool_array_indexer(array: AnyArrayLike, mask: AnyArrayLike) -> np.ndarray:
    "\n    Check if `mask` is a valid boolean indexer for `array`.\n\n    `array` and `mask` are checked to have the same length, and the\n    dtype is validated.\n\n    .. versionadded:: 1.0.0\n\n    Parameters\n    ----------\n    array : array\n        The array that's being masked.\n    mask : array\n        The boolean array that's masking.\n\n    Returns\n    -------\n    numpy.ndarray\n        The validated boolean mask.\n\n    Raises\n    ------\n    IndexError\n        When the lengths don't match.\n    ValueError\n        When `mask` cannot be converted to a bool-dtype ndarray.\n\n    See Also\n    --------\n    api.types.is_bool_dtype : Check if `key` is of boolean dtype.\n\n    Examples\n    --------\n    A boolean ndarray is returned when the arguments are all valid.\n\n    >>> mask = pd.array([True, False])\n    >>> arr = pd.array([1, 2])\n    >>> pd.api.extensions.check_bool_array_indexer(arr, mask)\n    array([ True, False])\n\n    An IndexError is raised when the lengths don't match.\n\n    >>> mask = pd.array([True, False, True])\n    >>> pd.api.extensions.check_bool_array_indexer(arr, mask)\n    Traceback (most recent call last):\n    ...\n    IndexError: Item wrong length 3 instead of 2.\n\n    A ValueError is raised when the mask cannot be converted to\n    a bool-dtype ndarray.\n\n    >>> mask = pd.array([True, pd.NA])\n    >>> pd.api.extensions.check_bool_array_indexer(arr, mask)\n    Traceback (most recent call last):\n    ...\n    ValueError: cannot convert to bool numpy array in presence of missing values\n    "
    result = np.asarray(mask, dtype=bool)
    if (len(result) != len(array)):
        raise IndexError(f'Item wrong length {len(result)} instead of {len(array)}.')
    return result
