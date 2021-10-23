def __getitem__(self, index):
    'x.__getitem__(i) <=> x[i]\n\n        Get an output of this symbol\n\n        Parameters\n        ----------\n        index : int or str\n            indexing key\n\n        '
    if isinstance(index, string_types):
        idx = None
        for (i, name) in enumerate(self.list_outputs()):
            if (name == index):
                if (idx is not None):
                    raise ValueError(('There are multiple outputs with name "%s"' % index))
                idx = i
        if (idx is None):
            raise ValueError(('Cannot find output that matches name "%s"' % index))
        index = idx
    if (not isinstance(index, int)):
        raise TypeError('Symbol only support integer index to fetch i-th output')
    if (index >= len(self.list_outputs())):
        raise IndexError
    handle = SymbolHandle()
    check_call(_LIB.MXSymbolGetOutput(self.handle, mx_uint(index), ctypes.byref(handle)))
    return Symbol(handle=handle)