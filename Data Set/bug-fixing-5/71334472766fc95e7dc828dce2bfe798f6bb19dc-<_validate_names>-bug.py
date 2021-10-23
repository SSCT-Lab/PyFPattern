def _validate_names(names):
    '\n    Check if the `names` parameter contains duplicates.\n\n    If duplicates are found, we issue a warning before returning.\n\n    Parameters\n    ----------\n    names : array-like or None\n        An array containing a list of the names used for the output DataFrame.\n\n    Returns\n    -------\n    names : array-like or None\n        The original `names` parameter.\n    '
    if (names is not None):
        if (len(names) != len(set(names))):
            raise ValueError('Duplicate names are not allowed.')
    return names