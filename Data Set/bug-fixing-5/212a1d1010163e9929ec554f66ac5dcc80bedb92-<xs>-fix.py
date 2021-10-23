def xs(self, key, axis=0, level=None, drop_level=True):
    "\n        Return cross-section from the Series/DataFrame.\n\n        This method takes a `key` argument to select data at a particular\n        level of a MultiIndex.\n\n        Parameters\n        ----------\n        key : label or tuple of label\n            Label contained in the index, or partially in a MultiIndex.\n        axis : {0 or 'index', 1 or 'columns'}, default 0\n            Axis to retrieve cross-section on.\n        level : object, defaults to first n levels (n=1 or len(key))\n            In case of a key partially contained in a MultiIndex, indicate\n            which levels are used. Levels can be referred by label or position.\n        drop_level : bool, default True\n            If False, returns object with same levels as self.\n\n        Returns\n        -------\n        Series or DataFrame\n            Cross-section from the original Series or DataFrame\n            corresponding to the selected index levels.\n\n        See Also\n        --------\n        DataFrame.loc : Access a group of rows and columns\n            by label(s) or a boolean array.\n        DataFrame.iloc : Purely integer-location based indexing\n            for selection by position.\n\n        Notes\n        -----\n        `xs` can not be used to set values.\n\n        MultiIndex Slicers is a generic way to get/set values on\n        any level or levels.\n        It is a superset of `xs` functionality, see\n        :ref:`MultiIndex Slicers <advanced.mi_slicers>`.\n\n        Examples\n        --------\n        >>> d = {'num_legs': [4, 4, 2, 2],\n        ...      'num_wings': [0, 0, 2, 2],\n        ...      'class': ['mammal', 'mammal', 'mammal', 'bird'],\n        ...      'animal': ['cat', 'dog', 'bat', 'penguin'],\n        ...      'locomotion': ['walks', 'walks', 'flies', 'walks']}\n        >>> df = pd.DataFrame(data=d)\n        >>> df = df.set_index(['class', 'animal', 'locomotion'])\n        >>> df\n                                   num_legs  num_wings\n        class  animal  locomotion\n        mammal cat     walks              4          0\n               dog     walks              4          0\n               bat     flies              2          2\n        bird   penguin walks              2          2\n\n        Get values at specified index\n\n        >>> df.xs('mammal')\n                           num_legs  num_wings\n        animal locomotion\n        cat    walks              4          0\n        dog    walks              4          0\n        bat    flies              2          2\n\n        Get values at several indexes\n\n        >>> df.xs(('mammal', 'dog'))\n                    num_legs  num_wings\n        locomotion\n        walks              4          0\n\n        Get values at specified index and level\n\n        >>> df.xs('cat', level=1)\n                           num_legs  num_wings\n        class  locomotion\n        mammal walks              4          0\n\n        Get values at several indexes and levels\n\n        >>> df.xs(('bird', 'walks'),\n        ...       level=[0, 'locomotion'])\n                 num_legs  num_wings\n        animal\n        penguin         2          2\n\n        Get values at specified column and axis\n\n        >>> df.xs('num_wings', axis=1)\n        class   animal   locomotion\n        mammal  cat      walks         0\n                dog      walks         0\n                bat      flies         2\n        bird    penguin  walks         2\n        Name: num_wings, dtype: int64\n        "
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