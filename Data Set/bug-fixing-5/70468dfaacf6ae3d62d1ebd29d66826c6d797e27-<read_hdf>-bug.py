def read_hdf(path_or_buf, key=None, mode='r', **kwargs):
    " read from the store, close it if we opened it\n\n        Retrieve pandas object stored in file, optionally based on where\n        criteria\n\n        Parameters\n        ----------\n        path_or_buf : path (string), buffer or path object (pathlib.Path or\n            py._path.local.LocalPath) designating the file to open, or an\n            already opened pd.HDFStore object\n\n            .. versionadded:: 0.19.0 support for pathlib, py.path.\n\n        key : group identifier in the store. Can be omitted if the HDF file\n            contains a single pandas object.\n        mode : string, {'r', 'r+', 'a'}, default 'r'. Mode to use when opening\n            the file. Ignored if path_or_buf is a pd.HDFStore.\n        where : list of Term (or convertible) objects, optional\n        start : optional, integer (defaults to None), row number to start\n            selection\n        stop  : optional, integer (defaults to None), row number to stop\n            selection\n        columns : optional, a list of columns that if not None, will limit the\n            return columns\n        iterator : optional, boolean, return an iterator, default False\n        chunksize : optional, nrows to include in iteration, return an iterator\n\n        Returns\n        -------\n        The selected object\n\n        "
    if (mode not in ['r', 'r+', 'a']):
        raise ValueError('mode {0} is not allowed while performing a read. Allowed modes are r, r+ and a.'.format(mode))
    if ('where' in kwargs):
        kwargs['where'] = _ensure_term(kwargs['where'], scope_level=1)
    if isinstance(path_or_buf, HDFStore):
        if (not path_or_buf.is_open):
            raise IOError('The HDFStore must be open for reading.')
        store = path_or_buf
        auto_close = False
    else:
        path_or_buf = _stringify_path(path_or_buf)
        if (not isinstance(path_or_buf, string_types)):
            raise NotImplementedError('Support for generic buffers has not been implemented.')
        try:
            exists = os.path.exists(path_or_buf)
        except (TypeError, ValueError):
            exists = False
        if (not exists):
            raise compat.FileNotFoundError(('File %s does not exist' % path_or_buf))
        store = HDFStore(path_or_buf, mode=mode, **kwargs)
        auto_close = True
    try:
        if (key is None):
            groups = store.groups()
            if (len(groups) == 0):
                raise ValueError('No dataset in HDF5 file.')
            candidate_only_group = groups[0]
            for group_to_check in groups[1:]:
                if (not _is_metadata_of(group_to_check, candidate_only_group)):
                    raise ValueError('key must be provided when HDF5 file contains multiple datasets.')
            key = candidate_only_group._v_pathname
        return store.select(key, auto_close=auto_close, **kwargs)
    except:
        try:
            store.close()
        except:
            pass
        raise