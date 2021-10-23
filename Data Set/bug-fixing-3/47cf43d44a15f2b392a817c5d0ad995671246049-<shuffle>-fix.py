def shuffle(*arrays, **options):
    "Shuffle arrays or sparse matrices in a consistent way\n\n    This is a convenience alias to ``resample(*arrays, replace=False)`` to do\n    random permutations of the collections.\n\n    Parameters\n    ----------\n    *arrays : sequence of indexable data-structures\n        Indexable data-structures can be arrays, lists, dataframes or scipy\n        sparse matrices with consistent first dimension.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        The seed of the pseudo random number generator to use when shuffling\n        the data.  If int, random_state is the seed used by the random number\n        generator; If RandomState instance, random_state is the random number\n        generator; If None, the random number generator is the RandomState\n        instance used by `np.random`.\n\n    n_samples : int, None by default\n        Number of samples to generate. If left to None this is\n        automatically set to the first dimension of the arrays.\n\n    Returns\n    -------\n    shuffled_arrays : sequence of indexable data-structures\n        Sequence of shuffled copies of the collections. The original arrays\n        are not impacted.\n\n    Examples\n    --------\n    It is possible to mix sparse and dense arrays in the same run::\n\n      >>> X = np.array([[1., 0.], [2., 1.], [0., 0.]])\n      >>> y = np.array([0, 1, 2])\n\n      >>> from scipy.sparse import coo_matrix\n      >>> X_sparse = coo_matrix(X)\n\n      >>> from sklearn.utils import shuffle\n      >>> X, X_sparse, y = shuffle(X, X_sparse, y, random_state=0)\n      >>> X\n      array([[ 0.,  0.],\n             [ 2.,  1.],\n             [ 1.,  0.]])\n\n      >>> X_sparse                   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE\n      <3x2 sparse matrix of type '<... 'numpy.float64'>'\n          with 3 stored elements in Compressed Sparse Row format>\n\n      >>> X_sparse.toarray()\n      array([[ 0.,  0.],\n             [ 2.,  1.],\n             [ 1.,  0.]])\n\n      >>> y\n      array([2, 1, 0])\n\n      >>> shuffle(y, n_samples=2, random_state=0)\n      array([0, 1])\n\n    See also\n    --------\n    :func:`sklearn.utils.resample`\n    "
    options['replace'] = False
    return resample(*arrays, **options)