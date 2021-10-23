

def set_index(self, keys, drop=True, append=False, inplace=False, verify_integrity=False):
    "\n        Set the DataFrame index using existing columns.\n\n        Set the DataFrame index (row labels) using one or more existing\n        columns. The index can replace the existing index or expand on it.\n\n        Parameters\n        ----------\n        keys : label or list of label\n            Name or names of the columns that will be used as the index.\n        drop : bool, default True\n            Delete columns to be used as the new index.\n        append : bool, default False\n            Whether to append columns to existing index.\n        inplace : bool, default False\n            Modify the DataFrame in place (do not create a new object).\n        verify_integrity : bool, default False\n            Check the new index for duplicates. Otherwise defer the check until\n            necessary. Setting to False will improve the performance of this\n            method.\n\n        Returns\n        -------\n        DataFrame\n            Changed row labels.\n\n        See Also\n        --------\n        DataFrame.reset_index : Opposite of set_index.\n        DataFrame.reindex : Change to new indices or expand indices.\n        DataFrame.reindex_like : Change to same indices as other DataFrame.\n\n        Returns\n        -------\n        DataFrame\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({'month': [1, 4, 7, 10],\n        ...                    'year': [2012, 2014, 2013, 2014],\n        ...                    'sale': [55, 40, 84, 31]})\n        >>> df\n           month  year  sale\n        0      1  2012    55\n        1      4  2014    40\n        2      7  2013    84\n        3     10  2014    31\n\n        Set the index to become the 'month' column:\n\n        >>> df.set_index('month')\n               year  sale\n        month\n        1      2012    55\n        4      2014    40\n        7      2013    84\n        10     2014    31\n\n        Create a multi-index using columns 'year' and 'month':\n\n        >>> df.set_index(['year', 'month'])\n                    sale\n        year  month\n        2012  1     55\n        2014  4     40\n        2013  7     84\n        2014  10    31\n\n        Create a multi-index using a set of values and a column:\n\n        >>> df.set_index([[1, 2, 3, 4], 'year'])\n                 month  sale\n           year\n        1  2012  1      55\n        2  2014  4      40\n        3  2013  7      84\n        4  2014  10     31\n        "
    inplace = validate_bool_kwarg(inplace, 'inplace')
    if (not isinstance(keys, list)):
        keys = [keys]
    missing = []
    for col in keys:
        if ((is_scalar(col) or isinstance(col, tuple)) and (col in self)):
            continue
        elif (is_scalar(col) and (col not in self)):
            missing.append(col)
        elif ((not is_list_like(col, allow_sets=False)) or (getattr(col, 'ndim', 1) > 1)):
            raise TypeError('The parameter "keys" may only contain a combination of valid column keys and one-dimensional list-likes')
    if missing:
        raise KeyError('{}'.format(missing))
    if inplace:
        frame = self
    else:
        frame = self.copy()
    arrays = []
    names = []
    if append:
        names = [x for x in self.index.names]
        if isinstance(self.index, ABCMultiIndex):
            for i in range(self.index.nlevels):
                arrays.append(self.index._get_level_values(i))
        else:
            arrays.append(self.index)
    to_remove = []
    for col in keys:
        if isinstance(col, ABCMultiIndex):
            for n in range(col.nlevels):
                arrays.append(col._get_level_values(n))
            names.extend(col.names)
        elif isinstance(col, (ABCIndexClass, ABCSeries)):
            arrays.append(col)
            names.append(col.name)
        elif isinstance(col, (list, np.ndarray)):
            arrays.append(col)
            names.append(None)
        elif (is_list_like(col) and (not (isinstance(col, tuple) and (col in self)))):
            col = list(col)
            arrays.append(col)
            names.append(None)
        else:
            arrays.append(frame[col]._values)
            names.append(col)
            if drop:
                to_remove.append(col)
    index = ensure_index_from_sequences(arrays, names)
    if (verify_integrity and (not index.is_unique)):
        duplicates = index[index.duplicated()].unique()
        raise ValueError('Index has duplicate keys: {dup}'.format(dup=duplicates))
    for c in set(to_remove):
        del frame[c]
    index._cleanup()
    frame.index = index
    if (not inplace):
        return frame
