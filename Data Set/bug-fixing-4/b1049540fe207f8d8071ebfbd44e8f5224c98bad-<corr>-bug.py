def corr(self, method='pearson', min_periods=1):
    "\n        Compute pairwise correlation of columns, excluding NA/null values.\n\n        Parameters\n        ----------\n        method : {'pearson', 'kendall', 'spearman'} or callable\n            Method of correlation:\n\n            * pearson : standard correlation coefficient\n            * kendall : Kendall Tau correlation coefficient\n            * spearman : Spearman rank correlation\n            * callable: callable with input two 1d ndarrays\n                and returning a float. Note that the returned matrix from corr\n                will have 1 along the diagonals and will be symmetric\n                regardless of the callable's behavior\n                .. versionadded:: 0.24.0\n\n        min_periods : int, optional\n            Minimum number of observations required per pair of columns\n            to have a valid result. Currently only available for Pearson\n            and Spearman correlation.\n\n        Returns\n        -------\n        DataFrame\n            Correlation matrix.\n\n        See Also\n        --------\n        DataFrame.corrwith\n        Series.corr\n\n        Examples\n        --------\n        >>> def histogram_intersection(a, b):\n        ...     v = np.minimum(a, b).sum().round(decimals=1)\n        ...     return v\n        >>> df = pd.DataFrame([(.2, .3), (.0, .6), (.6, .0), (.2, .1)],\n        ...                   columns=['dogs', 'cats'])\n        >>> df.corr(method=histogram_intersection)\n              dogs  cats\n        dogs   1.0   0.3\n        cats   0.3   1.0\n        "
    numeric_df = self._get_numeric_data()
    cols = numeric_df.columns
    idx = cols.copy()
    mat = numeric_df.values
    if (method == 'pearson'):
        correl = libalgos.nancorr(ensure_float64(mat), minp=min_periods)
    elif (method == 'spearman'):
        correl = libalgos.nancorr_spearman(ensure_float64(mat), minp=min_periods)
    elif ((method == 'kendall') or callable(method)):
        if (min_periods is None):
            min_periods = 1
        mat = ensure_float64(mat).T
        corrf = nanops.get_corr_func(method)
        K = len(cols)
        correl = np.empty((K, K), dtype=float)
        mask = np.isfinite(mat)
        for (i, ac) in enumerate(mat):
            for (j, bc) in enumerate(mat):
                if (i > j):
                    continue
                valid = (mask[i] & mask[j])
                if (valid.sum() < min_periods):
                    c = np.nan
                elif (i == j):
                    c = 1.0
                elif (not valid.all()):
                    c = corrf(ac[valid], bc[valid])
                else:
                    c = corrf(ac, bc)
                correl[(i, j)] = c
                correl[(j, i)] = c
    else:
        raise ValueError("method must be either 'pearson', 'spearman', 'kendall', or a callable, '{method}' was supplied".format(method=method))
    return self._constructor(correl, index=idx, columns=cols)