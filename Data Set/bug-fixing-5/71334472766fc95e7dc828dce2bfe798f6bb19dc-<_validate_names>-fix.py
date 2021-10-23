def _validate_names(names):
    '\n    Raise ValueError if the `names` parameter contains duplicates.\n\n    Parameters\n    ----------\n    names : array-like or None\n        An array containing a list of the names used for the output DataFrame.\n\n    Raises\n    ------\n    ValueError\n        If names are not unique.\n    '
    if (names is not None):
        if (len(names) != len(set(names))):
            raise ValueError('Duplicate names are not allowed.')