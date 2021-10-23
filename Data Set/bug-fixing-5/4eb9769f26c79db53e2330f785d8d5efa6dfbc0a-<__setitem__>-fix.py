def __setitem__(self, key, value):
    ' Item assignment.\n\n\n        Raises\n        ------\n        ValueError\n            If (one or more) Value is not in categories or if a assigned\n            `Categorical` does not have the same categories\n        '
    if isinstance(value, Categorical):
        if (not value.categories.equals(self.categories)):
            raise ValueError('Cannot set a Categorical with another, without identical categories')
    rvalue = (value if is_list_like(value) else [value])
    from pandas import Index
    to_add = Index(rvalue).difference(self.categories)
    if (len(to_add) and (not isna(to_add).all())):
        raise ValueError('Cannot setitem on a Categorical with a new category, set the categories first')
    if isinstance(key, (int, np.integer)):
        pass
    elif isinstance(key, tuple):
        if (len(key) == 2):
            if (not com.is_null_slice(key[0])):
                raise AssertionError('invalid slicing for a 1-ndim categorical')
            key = key[1]
        elif (len(key) == 1):
            key = key[0]
        else:
            raise AssertionError('invalid slicing for a 1-ndim categorical')
    elif isinstance(key, slice):
        pass
    else:
        key = np.asarray(key)
    lindexer = self.categories.get_indexer(rvalue)
    lindexer = self._maybe_coerce_indexer(lindexer)
    self._codes[key] = lindexer