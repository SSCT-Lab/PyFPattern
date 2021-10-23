def corrwith(self, other, axis=0, drop=False, method='pearson'):
    "\n        Compute pairwise correlation between rows or columns of DataFrame\n        with rows or columns of Series or DataFrame.  DataFrames are first\n        aligned along both axes before computing the correlations.\n\n        Parameters\n        ----------\n        other : DataFrame, Series\n            Object with which to compute correlations.\n        axis : {0 or 'index', 1 or 'columns'}, default 0\n            The axis to use. 0 or 'index' to compute column-wise, 1 or 'columns' for\n            row-wise.\n        drop : bool, default False\n            Drop missing indices from result.\n        method : {'pearson', 'kendall', 'spearman'} or callable\n            Method of correlation:\n\n            * pearson : standard correlation coefficient\n            * kendall : Kendall Tau correlation coefficient\n            * spearman : Spearman rank correlation\n            * callable: callable with input two 1d ndarrays\n                and returning a float.\n\n            .. versionadded:: 0.24.0\n\n        Returns\n        -------\n        Series\n            Pairwise correlations.\n\n        See Also\n        --------\n        DataFrame.corr\n        "
    axis = self._get_axis_number(axis)
    this = self._get_numeric_data()
    if isinstance(other, Series):
        return this.apply((lambda x: other.corr(x, method=method)), axis=axis)
    other = other._get_numeric_data()
    (left, right) = this.align(other, join='inner', copy=False)
    if (axis == 1):
        left = left.T
        right = right.T
    if (method == 'pearson'):
        left = (left + (right * 0))
        right = (right + (left * 0))
        ldem = (left - left.mean())
        rdem = (right - right.mean())
        num = (ldem * rdem).sum()
        dom = (((left.count() - 1) * left.std()) * right.std())
        correl = (num / dom)
    elif ((method in ['kendall', 'spearman']) or callable(method)):

        def c(x):
            return nanops.nancorr(x[0], x[1], method=method)
        correl = Series(map(c, zip(left.values.T, right.values.T)), index=left.columns)
    else:
        raise ValueError("Invalid method {method} was passed, valid methods are: 'pearson', 'kendall', 'spearman', or callable".format(method=method))
    if (not drop):
        raxis = (1 if (axis == 0) else 0)
        result_index = this._get_axis(raxis).union(other._get_axis(raxis))
        idx_diff = result_index.difference(correl.index)
        if (len(idx_diff) > 0):
            correl = correl.append(Series(([np.nan] * len(idx_diff)), index=idx_diff))
    return correl