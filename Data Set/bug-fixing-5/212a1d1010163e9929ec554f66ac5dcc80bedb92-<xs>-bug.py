def xs(self, key, axis=0, level=None, drop_level=True):
    "\n        Returns a cross-section (row(s) or column(s)) from the\n        Series/DataFrame. Defaults to cross-section on the rows (axis=0).\n\n        Parameters\n        ----------\n        key : object\n            Some label contained in the index, or partially in a MultiIndex\n        axis : int, default 0\n            Axis to retrieve cross-section on\n        level : object, defaults to first n levels (n=1 or len(key))\n            In case of a key partially contained in a MultiIndex, indicate\n            which levels are used. Levels can be referred by label or position.\n        drop_level : boolean, default True\n            If False, returns object with same levels as self.\n\n        Examples\n        --------\n        >>> df\n           A  B  C\n        a  4  5  2\n        b  4  0  9\n        c  9  7  3\n        >>> df.xs('a')\n        A    4\n        B    5\n        C    2\n        Name: a\n        >>> df.xs('C', axis=1)\n        a    2\n        b    9\n        c    3\n        Name: C\n\n        >>> df\n                            A  B  C  D\n        first second third\n        bar   one    1      4  1  8  9\n              two    1      7  5  5  0\n        baz   one    1      6  6  8  0\n              three  2      5  3  5  3\n        >>> df.xs(('baz', 'three'))\n               A  B  C  D\n        third\n        2      5  3  5  3\n        >>> df.xs('one', level=1)\n                     A  B  C  D\n        first third\n        bar   1      4  1  8  9\n        baz   1      6  6  8  0\n        >>> df.xs(('baz', 2), level=[0, 'third'])\n                A  B  C  D\n        second\n        three   5  3  5  3\n\n        Returns\n        -------\n        xs : Series or DataFrame\n\n        Notes\n        -----\n        xs is only for getting, not setting values.\n\n        MultiIndex Slicers is a generic way to get/set values on any level or\n        levels.  It is a superset of xs functionality, see\n        :ref:`MultiIndex Slicers <advanced.mi_slicers>`\n        "
    axis = self._get_axis_number(axis)
    labels = self._get_axis(axis)
    if (level is not None):
        (loc, new_ax) = labels.get_loc_level(key, level=level, drop_level=drop_level)
        indexer = ([slice(None)] * self.ndim)
        indexer[axis] = loc
        indexer = tuple(indexer)
        result = self.iloc[indexer]
        setattr(result, result._get_axis_name(axis), new_ax)
        return result
    if (axis == 1):
        return self[key]
    self._consolidate_inplace()
    index = self.index
    if isinstance(index, MultiIndex):
        (loc, new_index) = self.index.get_loc_level(key, drop_level=drop_level)
    else:
        loc = self.index.get_loc(key)
        if isinstance(loc, np.ndarray):
            if (loc.dtype == np.bool_):
                (inds,) = loc.nonzero()
                return self._take(inds, axis=axis)
            else:
                return self._take(loc, axis=axis)
        if (not is_scalar(loc)):
            new_index = self.index[loc]
    if is_scalar(loc):
        new_values = self._data.fast_xs(loc)
        if ((not is_list_like(new_values)) or (self.ndim == 1)):
            return com.maybe_box_datetimelike(new_values)
        result = self._constructor_sliced(new_values, index=self.columns, name=self.index[loc], dtype=new_values.dtype)
    else:
        result = self.iloc[loc]
        result.index = new_index
    result._set_is_copy(self, copy=(not result._is_view))
    return result