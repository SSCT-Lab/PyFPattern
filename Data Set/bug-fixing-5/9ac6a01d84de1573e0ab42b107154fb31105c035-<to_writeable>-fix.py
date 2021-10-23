def to_writeable(source):
    ' Convert input object ``source`` to something we can write\n\n    Parameters\n    ----------\n    source : object\n\n    Returns\n    -------\n    arr : None or ndarray or EmptyStructMarker\n        If `source` cannot be converted to something we can write to a matfile,\n        return None.  If `source` is equivalent to an empty dictionary, return\n        ``EmptyStructMarker``.  Otherwise return `source` converted to an\n        ndarray with contents for writing to matfile.\n    '
    if isinstance(source, np.ndarray):
        return source
    if (source is None):
        return None
    is_mapping = (hasattr(source, 'keys') and hasattr(source, 'values') and hasattr(source, 'items'))
    if isinstance(source, np.generic):
        pass
    elif ((not is_mapping) and hasattr(source, '__dict__')):
        source = dict(((key, value) for (key, value) in source.__dict__.items() if (not key.startswith('_'))))
        is_mapping = True
    if is_mapping:
        dtype = []
        values = []
        for (field, value) in source.items():
            if (isinstance(field, string_types) and (field[0] not in '_0123456789')):
                dtype.append((str(field), object))
                values.append(value)
        if dtype:
            return np.array([tuple(values)], dtype)
        else:
            return EmptyStructMarker
    narr = np.asanyarray(source)
    if ((narr.dtype.type in (object, np.object_)) and (narr.shape == ()) and (narr == source)):
        return None
    return narr