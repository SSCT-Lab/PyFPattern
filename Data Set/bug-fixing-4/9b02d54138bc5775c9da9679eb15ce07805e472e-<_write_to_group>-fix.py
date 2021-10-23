def _write_to_group(self, key: str, value, format, axes=None, index=True, append=False, complib=None, complevel: Optional[int]=None, fletcher32=None, min_itemsize=None, chunksize=None, expectedrows=None, dropna=False, nan_rep=None, data_columns=None, encoding=None, errors: str='strict'):
    group = self.get_node(key)
    assert (self._handle is not None)
    if ((group is not None) and (not append)):
        self._handle.remove_node(group, recursive=True)
        group = None
    if (getattr(value, 'empty', None) and ((format == 'table') or append)):
        return
    if (group is None):
        paths = key.split('/')
        path = '/'
        for p in paths:
            if (not len(p)):
                continue
            new_path = path
            if (not path.endswith('/')):
                new_path += '/'
            new_path += p
            group = self.get_node(new_path)
            if (group is None):
                group = self._handle.create_group(path, p)
            path = new_path
    s = self._create_storer(group, format, value, encoding=encoding, errors=errors)
    if append:
        if ((not s.is_table) or (s.is_table and (format == 'fixed') and s.is_exists)):
            raise ValueError('Can only append to Tables')
        if (not s.is_exists):
            s.set_object_info()
    else:
        s.set_object_info()
    if ((not s.is_table) and complib):
        raise ValueError('Compression not supported on Fixed format stores')
    s.write(obj=value, axes=axes, append=append, complib=complib, complevel=complevel, fletcher32=fletcher32, min_itemsize=min_itemsize, chunksize=chunksize, expectedrows=expectedrows, dropna=dropna, nan_rep=nan_rep, data_columns=data_columns)
    if (isinstance(s, Table) and index):
        s.create_index(columns=index)