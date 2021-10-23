

def read_hdf(path_or_buf, key=None, mode='r', **kwargs):
    "\n    Read from the store, close it if we opened it.\n\n    Retrieve pandas object stored in file, optionally based on where\n    criteria\n\n    Parameters\n    ----------\n    path_or_buf : string, buffer or path object\n        Path to the file to open, or an open :class:`pandas.HDFStore` object.\n        Supports any object implementing the ``__fspath__`` protocol.\n        This includes :class:`pathlib.Path` and py._path.local.LocalPath\n        objects.\n\n        .. versionadded:: 0.19.0 support for pathlib, py.path.\n        .. versionadded:: 0.21.0 support for __fspath__ proptocol.\n\n    key : object, optional\n        The group identifier in the store. Can be omitted if the HDF file\n        contains a single pandas object.\n    mode : {'r', 'r+', 'a'}, optional\n        Mode to use when opening the file. Ignored if path_or_buf is a\n        :class:`pandas.HDFStore`. Default is 'r'.\n    where : list, optional\n        A list of Term (or convertible) objects.\n    start : int, optional\n        Row number to start selection.\n    stop  : int, optional\n        Row number to stop selection.\n    columns : list, optional\n        A list of columns names to return.\n    iterator : bool, optional\n        Return an iterator object.\n    chunksize : int, optional\n        Number of rows to include in an iteration when using an iterator.\n    kwargs : dict\n        Additional keyword arguments passed to HDFStore.\n\n    Returns\n    -------\n    item : object\n        The selected object. Return type depends on the object stored.\n\n    See Also\n    --------\n    pandas.DataFrame.to_hdf : write a HDF file from a DataFrame\n    pandas.HDFStore : low-level access to HDF files\n\n    Examples\n    --------\n    >>> df = pd.DataFrame([[1, 1.0, 'a']], columns=['x', 'y', 'z'])\n    >>> df.to_hdf('./store.h5', 'data')\n    >>> reread = pd.read_hdf('./store.h5')\n    "
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
