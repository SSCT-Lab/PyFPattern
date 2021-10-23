def append(self, other, ignore_index=False, verify_integrity=False):
    "\n        Append rows of `other` to the end of this frame, returning a new\n        object. Columns not in this frame are added as new columns.\n\n        Parameters\n        ----------\n        other : DataFrame or Series/dict-like object, or list of these\n            The data to append.\n        ignore_index : boolean, default False\n            If True, do not use the index labels.\n        verify_integrity : boolean, default False\n            If True, raise ValueError on creating index with duplicates.\n\n        Returns\n        -------\n        appended : DataFrame\n\n        Notes\n        -----\n        If a list of dict/series is passed and the keys are all contained in\n        the DataFrame's index, the order of the columns in the resulting\n        DataFrame will be unchanged.\n\n        Iteratively appending rows to a DataFrame can be more computationally\n        intensive than a single concatenate. A better solution is to append\n        those rows to a list and then concatenate the list with the original\n        DataFrame all at once.\n\n        See also\n        --------\n        pandas.concat : General function to concatenate DataFrame, Series\n            or Panel objects\n\n        Examples\n        --------\n\n        >>> df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))\n        >>> df\n           A  B\n        0  1  2\n        1  3  4\n        >>> df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))\n        >>> df.append(df2)\n           A  B\n        0  1  2\n        1  3  4\n        0  5  6\n        1  7  8\n\n        With `ignore_index` set to True:\n\n        >>> df.append(df2, ignore_index=True)\n           A  B\n        0  1  2\n        1  3  4\n        2  5  6\n        3  7  8\n\n        The following, while not recommended methods for generating DataFrames,\n        show two ways to generate a DataFrame from multiple data sources.\n\n        Less efficient:\n\n        >>> df = pd.DataFrame(columns=['A'])\n        >>> for i in range(5):\n        ...     df = df.append({'A'}: i}, ignore_index=True)\n        >>> df\n           A\n        0  0\n        1  1\n        2  2\n        3  3\n        4  4\n\n        More efficient:\n\n        >>> pd.concat([pd.DataFrame([i], columns=['A']) for i in range(5)],\n        ...           ignore_index=True)\n           A\n        0  0\n        1  1\n        2  2\n        3  3\n        4  4\n\n        "
    if isinstance(other, (Series, dict)):
        if isinstance(other, dict):
            other = Series(other)
        if ((other.name is None) and (not ignore_index)):
            raise TypeError('Can only append a Series if ignore_index=True or if the Series has a name')
        if (other.name is None):
            index = None
        else:
            index = Index([other.name], name=self.index.name)
        combined_columns = (self.columns.tolist() + self.columns.union(other.index).difference(self.columns).tolist())
        other = other.reindex(combined_columns, copy=False)
        other = DataFrame(other.values.reshape((1, len(other))), index=index, columns=combined_columns)
        other = other._convert(datetime=True, timedelta=True)
        if (not self.columns.equals(combined_columns)):
            self = self.reindex(columns=combined_columns)
    elif (isinstance(other, list) and (not isinstance(other[0], DataFrame))):
        other = DataFrame(other)
        if (self.columns.get_indexer(other.columns) >= 0).all():
            other = other.loc[:, self.columns]
    from pandas.core.reshape.concat import concat
    if isinstance(other, (list, tuple)):
        to_concat = ([self] + other)
    else:
        to_concat = [self, other]
    return concat(to_concat, ignore_index=ignore_index, verify_integrity=verify_integrity)