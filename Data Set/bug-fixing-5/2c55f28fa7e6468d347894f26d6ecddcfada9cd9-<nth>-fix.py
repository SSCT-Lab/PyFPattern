@Substitution(name='groupby')
@Appender(_doc_template)
def nth(self, n, dropna=None):
    "\n        Take the nth row from each group if n is an int, or a subset of rows\n        if n is a list of ints.\n\n        If dropna, will take the nth non-null row, dropna is either\n        Truthy (if a Series) or 'all', 'any' (if a DataFrame);\n        this is equivalent to calling dropna(how=dropna) before the\n        groupby.\n\n        Parameters\n        ----------\n        n : int or list of ints\n            a single nth value for the row or a list of nth values\n        dropna : None or str, optional\n            apply the specified dropna operation before counting which row is\n            the nth row. Needs to be None, 'any' or 'all'\n\n        Examples\n        --------\n\n        >>> df = pd.DataFrame({'A': [1, 1, 2, 1, 2],\n        ...                    'B': [np.nan, 2, 3, 4, 5]}, columns=['A', 'B'])\n        >>> g = df.groupby('A')\n        >>> g.nth(0)\n             B\n        A\n        1  NaN\n        2  3.0\n        >>> g.nth(1)\n             B\n        A\n        1  2.0\n        2  5.0\n        >>> g.nth(-1)\n             B\n        A\n        1  4.0\n        2  5.0\n        >>> g.nth([0, 1])\n             B\n        A\n        1  NaN\n        1  2.0\n        2  3.0\n        2  5.0\n\n        Specifying ``dropna`` allows count ignoring NaN\n\n        >>> g.nth(0, dropna='any')\n             B\n        A\n        1  2.0\n        2  3.0\n\n        NaNs denote group exhausted when using dropna\n\n        >>> g.nth(3, dropna='any')\n            B\n        A\n        1 NaN\n        2 NaN\n\n        Specifying ``as_index=False`` in ``groupby`` keeps the original index.\n\n        >>> df.groupby('A', as_index=False).nth(1)\n           A    B\n        1  1  2.0\n        4  2  5.0\n        "
    if isinstance(n, int):
        nth_values = [n]
    elif isinstance(n, (set, list, tuple)):
        nth_values = list(set(n))
        if (dropna is not None):
            raise ValueError('dropna option with a list of nth values is not supported')
    else:
        raise TypeError('n needs to be an int or a list/set/tuple of ints')
    nth_values = np.array(nth_values, dtype=np.intp)
    self._set_group_selection()
    if (not dropna):
        mask = (np.in1d(self._cumcount_array(), nth_values) | np.in1d((self._cumcount_array(ascending=False) + 1), (- nth_values)))
        out = self._selected_obj[mask]
        if (not self.as_index):
            return out
        (ids, _, _) = self.grouper.group_info
        out.index = self.grouper.result_index[ids[mask]]
        return (out.sort_index() if self.sort else out)
    if (isinstance(self._selected_obj, DataFrame) and (dropna not in ['any', 'all'])):
        raise ValueError(("For a DataFrame groupby, dropna must be either None, 'any' or 'all', (was passed %s)." % dropna))
    max_len = (n if (n >= 0) else ((- 1) - n))
    dropped = self.obj.dropna(how=dropna, axis=self.axis)
    if ((self.keys is None) and (self.level is None)):
        axis = self.grouper.axis
        grouper = axis[axis.isin(dropped.index)]
    else:
        (grouper, _, _) = _get_grouper(dropped, key=self.keys, axis=self.axis, level=self.level, sort=self.sort, mutated=self.mutated)
    grb = dropped.groupby(grouper, as_index=self.as_index, sort=self.sort)
    (sizes, result) = (grb.size(), grb.nth(n))
    mask = (sizes < max_len).values
    if (len(result) and mask.any()):
        result.loc[mask] = np.nan
    if ((len(self.obj) == len(dropped)) or (len(result) == len(self.grouper.result_index))):
        result.index = self.grouper.result_index
    else:
        result = result.reindex(self.grouper.result_index)
    return result