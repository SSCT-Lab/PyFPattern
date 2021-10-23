

def stack(self, level=(- 1), dropna=True):
    "\n        Stack the prescribed level(s) from columns to index.\n\n        Return a reshaped DataFrame or Series having a multi-level\n        index with one or more new inner-most levels compared to the current\n        DataFrame. The new inner-most levels are created by pivoting the\n        columns of the current dataframe:\n\n          - if the columns have a single level, the output is a Series;\n          - if the columns have multiple levels, the new index\n            level(s) is (are) taken from the prescribed level(s) and\n            the output is a DataFrame.\n\n        The new index levels are sorted.\n\n        Parameters\n        ----------\n        level : int, str, list, default -1\n            Level(s) to stack from the column axis onto the index\n            axis, defined as one index or label, or a list of indices\n            or labels.\n        dropna : bool, default True\n            Whether to drop rows in the resulting Frame/Series with\n            missing values. Stacking a column level onto the index\n            axis can create combinations of index and column values\n            that are missing from the original dataframe. See Examples\n            section.\n\n        Returns\n        -------\n        DataFrame or Series\n            Stacked dataframe or series.\n\n        See Also\n        --------\n        DataFrame.unstack : Unstack prescribed level(s) from index axis\n             onto column axis.\n        DataFrame.pivot : Reshape dataframe from long format to wide\n             format.\n        DataFrame.pivot_table : Create a spreadsheet-style pivot table\n             as a DataFrame.\n\n        Notes\n        -----\n        The function is named by analogy with a collection of books\n        being re-organised from being side by side on a horizontal\n        position (the columns of the dataframe) to being stacked\n        vertically on top of of each other (in the index of the\n        dataframe).\n\n        Examples\n        --------\n        **Single level columns**\n\n        >>> df_single_level_cols = pd.DataFrame([[0, 1], [2, 3]],\n        ...                                     index=['cat', 'dog'],\n        ...                                     columns=['weight', 'height'])\n\n        Stacking a dataframe with a single level column axis returns a Series:\n\n        >>> df_single_level_cols\n             weight height\n        cat       0      1\n        dog       2      3\n        >>> df_single_level_cols.stack()\n        cat  weight    0\n             height    1\n        dog  weight    2\n             height    3\n        dtype: int64\n\n        **Multi level columns: simple case**\n\n        >>> multicol1 = pd.MultiIndex.from_tuples([('weight', 'kg'),\n        ...                                        ('weight', 'pounds')])\n        >>> df_multi_level_cols1 = pd.DataFrame([[1, 2], [2, 4]],\n        ...                                     index=['cat', 'dog'],\n        ...                                     columns=multicol1)\n\n        Stacking a dataframe with a multi-level column axis:\n\n        >>> df_multi_level_cols1\n             weight\n                 kg    pounds\n        cat       1        2\n        dog       2        4\n        >>> df_multi_level_cols1.stack()\n                    weight\n        cat kg           1\n            pounds       2\n        dog kg           2\n            pounds       4\n\n        **Missing values**\n\n        >>> multicol2 = pd.MultiIndex.from_tuples([('weight', 'kg'),\n        ...                                        ('height', 'm')])\n        >>> df_multi_level_cols2 = pd.DataFrame([[1.0, 2.0], [3.0, 4.0]],\n        ...                                     index=['cat', 'dog'],\n        ...                                     columns=multicol2)\n\n        It is common to have missing values when stacking a dataframe\n        with multi-level columns, as the stacked dataframe typically\n        has more values than the original dataframe. Missing values\n        are filled with NaNs:\n\n        >>> df_multi_level_cols2\n            weight height\n                kg      m\n        cat    1.0    2.0\n        dog    3.0    4.0\n        >>> df_multi_level_cols2.stack()\n                height  weight\n        cat kg     NaN     1.0\n            m      2.0     NaN\n        dog kg     NaN     3.0\n            m      4.0     NaN\n\n        **Prescribing the level(s) to be stacked**\n\n        The first parameter controls which level or levels are stacked:\n\n        >>> df_multi_level_cols2.stack(0)\n                     kg    m\n        cat height  NaN  2.0\n            weight  1.0  NaN\n        dog height  NaN  4.0\n            weight  3.0  NaN\n        >>> df_multi_level_cols2.stack([0, 1])\n        cat  height  m     2.0\n             weight  kg    1.0\n        dog  height  m     4.0\n             weight  kg    3.0\n        dtype: float64\n\n        **Dropping missing values**\n\n        >>> df_multi_level_cols3 = pd.DataFrame([[None, 1.0], [2.0, 3.0]],\n        ...                                     index=['cat', 'dog'],\n        ...                                     columns=multicol2)\n\n        Note that rows where all values are missing are dropped by\n        default but this behaviour can be controlled via the dropna\n        keyword parameter:\n\n        >>> df_multi_level_cols3\n            weight height\n                kg      m\n        cat    NaN    1.0\n        dog    2.0    3.0\n        >>> df_multi_level_cols3.stack(dropna=False)\n                height  weight\n        cat kg     NaN     NaN\n            m      1.0     NaN\n        dog kg     NaN     2.0\n            m      3.0     NaN\n        >>> df_multi_level_cols3.stack(dropna=True)\n                height  weight\n        cat m      1.0     NaN\n        dog kg     NaN     2.0\n            m      3.0     NaN\n        "
    from pandas.core.reshape.reshape import stack, stack_multiple
    if isinstance(level, (tuple, list)):
        return stack_multiple(self, level, dropna=dropna)
    else:
        return stack(self, level, dropna=dropna)
