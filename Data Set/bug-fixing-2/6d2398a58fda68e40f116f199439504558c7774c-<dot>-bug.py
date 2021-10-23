

def dot(self, other):
    '\n        Compute the matrix mutiplication between the DataFrame and other.\n\n        This method computes the matrix product between the DataFrame and the\n        values of an other Series, DataFrame or a numpy array.\n\n        It can also be called using ``self @ other`` in Python >= 3.5.\n\n        Parameters\n        ----------\n        other : Series, DataFrame or array-like\n            The other object to compute the matrix product with.\n\n        Returns\n        -------\n        Series or DataFrame\n            If other is a Series, return the matrix product between self and\n            other as a Serie. If other is a DataFrame or a numpy.array, return\n            the matrix product of self and other in a DataFrame of a np.array.\n\n        See Also\n        --------\n        Series.dot: Similar method for Series.\n\n        Notes\n        -----\n        The dimensions of DataFrame and other must be compatible in order to\n        compute the matrix multiplication.\n\n        The dot method for Series computes the inner product, instead of the\n        matrix product here.\n\n        Examples\n        --------\n        Here we multiply a DataFrame with a Series.\n\n        >>> df = pd.DataFrame([[0, 1, -2, -1], [1, 1, 1, 1]])\n        >>> s = pd.Series([1, 1, 2, 1])\n        >>> df.dot(s)\n        0    -4\n        1     5\n        dtype: int64\n\n        Here we multiply a DataFrame with another DataFrame.\n\n        >>> other = pd.DataFrame([[0, 1], [1, 2], [-1, -1], [2, 0]])\n        >>> df.dot(other)\n            0   1\n        0   1   4\n        1   2   2\n\n        Note that the dot method give the same result as @\n\n        >>> df @ other\n            0   1\n        0   1   4\n        1   2   2\n\n        The dot method works also if other is an np.array.\n\n        >>> arr = np.array([[0, 1], [1, 2], [-1, -1], [2, 0]])\n        >>> df.dot(arr)\n            0   1\n        0   1   4\n        1   2   2\n        '
    if isinstance(other, (Series, DataFrame)):
        common = self.columns.union(other.index)
        if ((len(common) > len(self.columns)) or (len(common) > len(other.index))):
            raise ValueError('matrices are not aligned')
        left = self.reindex(columns=common, copy=False)
        right = other.reindex(index=common, copy=False)
        lvals = left.values
        rvals = right.values
    else:
        left = self
        lvals = self.values
        rvals = np.asarray(other)
        if (lvals.shape[1] != rvals.shape[0]):
            raise ValueError('Dot product shape mismatch, {s} vs {r}'.format(s=lvals.shape, r=rvals.shape))
    if isinstance(other, DataFrame):
        return self._constructor(np.dot(lvals, rvals), index=left.index, columns=other.columns)
    elif isinstance(other, Series):
        return Series(np.dot(lvals, rvals), index=left.index)
    elif isinstance(rvals, (np.ndarray, Index)):
        result = np.dot(lvals, rvals)
        if (result.ndim == 2):
            return self._constructor(result, index=left.index)
        else:
            return Series(result, index=left.index)
    else:
        raise TypeError('unsupported type: {oth}'.format(oth=type(other)))
