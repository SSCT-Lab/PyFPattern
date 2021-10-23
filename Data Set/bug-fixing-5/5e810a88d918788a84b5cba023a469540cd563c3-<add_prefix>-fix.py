def add_prefix(self, prefix: str):
    "\n        Prefix labels with string `prefix`.\n\n        For Series, the row labels are prefixed.\n        For DataFrame, the column labels are prefixed.\n\n        Parameters\n        ----------\n        prefix : str\n            The string to add before each label.\n\n        Returns\n        -------\n        Series or DataFrame\n            New Series or DataFrame with updated labels.\n\n        See Also\n        --------\n        Series.add_suffix: Suffix row labels with string `suffix`.\n        DataFrame.add_suffix: Suffix column labels with string `suffix`.\n\n        Examples\n        --------\n        >>> s = pd.Series([1, 2, 3, 4])\n        >>> s\n        0    1\n        1    2\n        2    3\n        3    4\n        dtype: int64\n\n        >>> s.add_prefix('item_')\n        item_0    1\n        item_1    2\n        item_2    3\n        item_3    4\n        dtype: int64\n\n        >>> df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [3, 4, 5, 6]})\n        >>> df\n           A  B\n        0  1  3\n        1  2  4\n        2  3  5\n        3  4  6\n\n        >>> df.add_prefix('col_')\n             col_A  col_B\n        0       1       3\n        1       2       4\n        2       3       5\n        3       4       6\n        "
    f = functools.partial('{prefix}{}'.format, prefix=prefix)
    mapper = {
        self._info_axis_name: f,
    }
    return self.rename(**mapper)