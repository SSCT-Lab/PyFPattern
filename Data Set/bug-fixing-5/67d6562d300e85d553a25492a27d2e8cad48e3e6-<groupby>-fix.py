def groupby(self, by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, squeeze=False, observed=False, **kwargs):
    '\n        Group DataFrame or Series using a mapper or by a Series of columns.\n\n        A groupby operation involves some combination of splitting the\n        object, applying a function, and combining the results. This can be\n        used to group large amounts of data and compute operations on these\n        groups.\n\n        Parameters\n        ----------\n        by : mapping, function, label, or list of labels\n            Used to determine the groups for the groupby.\n            If ``by`` is a function, it\'s called on each value of the object\'s\n            index. If a dict or Series is passed, the Series or dict VALUES\n            will be used to determine the groups (the Series\' values are first\n            aligned; see ``.align()`` method). If an ndarray is passed, the\n            values are used as-is determine the groups. A label or list of\n            labels may be passed to group by the columns in ``self``. Notice\n            that a tuple is interpreted as a (single) key.\n        axis : {0 or \'index\', 1 or \'columns\'}, default 0\n            Split along rows (0) or columns (1).\n        level : int, level name, or sequence of such, default None\n            If the axis is a MultiIndex (hierarchical), group by a particular\n            level or levels.\n        as_index : bool, default True\n            For aggregated output, return object with group labels as the\n            index. Only relevant for DataFrame input. as_index=False is\n            effectively "SQL-style" grouped output.\n        sort : bool, default True\n            Sort group keys. Get better performance by turning this off.\n            Note this does not influence the order of observations within each\n            group. Groupby preserves the order of rows within each group.\n        group_keys : bool, default True\n            When calling apply, add group keys to index to identify pieces.\n        squeeze : bool, default False\n            Reduce the dimensionality of the return type if possible,\n            otherwise return a consistent type.\n        observed : bool, default False\n            This only applies if any of the groupers are Categoricals.\n            If True: only show observed values for categorical groupers.\n            If False: show all values for categorical groupers.\n\n            .. versionadded:: 0.23.0\n\n        **kwargs\n            Optional, only accepts keyword argument \'mutated\' and is passed\n            to groupby.\n\n        Returns\n        -------\n        DataFrameGroupBy or SeriesGroupBy\n            Depends on the calling object and returns groupby object that\n            contains information about the groups.\n\n        See Also\n        --------\n        resample : Convenience method for frequency conversion and resampling\n            of time series.\n\n        Notes\n        -----\n        See the `user guide\n        <http://pandas.pydata.org/pandas-docs/stable/groupby.html>`_ for more.\n\n        Examples\n        --------\n        >>> df = pd.DataFrame({\'Animal\': [\'Falcon\', \'Falcon\',\n        ...                               \'Parrot\', \'Parrot\'],\n        ...                    \'Max Speed\': [380., 370., 24., 26.]})\n        >>> df\n           Animal  Max Speed\n        0  Falcon      380.0\n        1  Falcon      370.0\n        2  Parrot       24.0\n        3  Parrot       26.0\n        >>> df.groupby([\'Animal\']).mean()\n                Max Speed\n        Animal\n        Falcon      375.0\n        Parrot       25.0\n\n        **Hierarchical Indexes**\n\n        We can groupby different levels of a hierarchical index\n        using the `level` parameter:\n\n        >>> arrays = [[\'Falcon\', \'Falcon\', \'Parrot\', \'Parrot\'],\n        ...           [\'Captive\', \'Wild\', \'Captive\', \'Wild\']]\n        >>> index = pd.MultiIndex.from_arrays(arrays, names=(\'Animal\', \'Type\'))\n        >>> df = pd.DataFrame({\'Max Speed\': [390., 350., 30., 20.]},\n        ...                   index=index)\n        >>> df\n                        Max Speed\n        Animal Type\n        Falcon Captive      390.0\n               Wild         350.0\n        Parrot Captive       30.0\n               Wild          20.0\n        >>> df.groupby(level=0).mean()\n                Max Speed\n        Animal\n        Falcon      370.0\n        Parrot       25.0\n        >>> df.groupby(level=1).mean()\n                 Max Speed\n        Type\n        Captive      210.0\n        Wild         185.0\n        '
    from pandas.core.groupby.groupby import groupby
    if ((level is None) and (by is None)):
        raise TypeError("You have to supply one of 'by' and 'level'")
    axis = self._get_axis_number(axis)
    return groupby(self, by=by, axis=axis, level=level, as_index=as_index, sort=sort, group_keys=group_keys, squeeze=squeeze, observed=observed, **kwargs)