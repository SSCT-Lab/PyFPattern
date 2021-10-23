def diagonal(self, k=0):
    'Returns the k-th diagonal of the matrix.\n\n        Parameters\n        ----------\n        k : int, optional\n            Which diagonal to get, corresponding to elements a[i, i+k].\n            Default: 0 (the main diagonal).\n\n            .. versionadded:: 1.0\n\n        See also\n        --------\n        numpy.diagonal : Equivalent numpy function.\n\n        Examples\n        --------\n        >>> from scipy.sparse import csr_matrix\n        >>> A = csr_matrix([[1, 2, 0], [0, 0, 3], [4, 0, 5]])\n        >>> A.diagonal()\n        array([1, 0, 5])\n        >>> A.diagonal(k=1)\n        array([2, 3])\n        '
    return self.tocsr().diagonal(k=k)