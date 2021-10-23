def resample(*arrays, **options):
    "Resample arrays or sparse matrices in a consistent way\n\n    The default strategy implements one step of the bootstrapping\n    procedure.\n\n    Parameters\n    ----------\n    *arrays : sequence of indexable data-structures\n        Indexable data-structures can be arrays, lists, dataframes or scipy\n        sparse matrices with consistent first dimension.\n\n    replace : boolean, True by default\n        Implements resampling with replacement. If False, this will implement\n        (sliced) random permutations.\n\n    n_samples : int, None by default\n        Number of samples to generate. If left to None this is\n        automatically set to the first dimension of the arrays.\n        If replace is False it should not be larger than the length of\n        arrays.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        The seed of the pseudo random number generator to use when shuffling\n        the data.  If int, random_state is the seed used by the random number\n        generator; If RandomState instance, random_state is the random number\n        generator; If None, the random number generator is the RandomState\n        instance used by `np.random`.\n\n    Returns\n    -------\n    resampled_arrays : sequence of indexable data-structures\n        Sequence of resampled copies of the collections. The original arrays\n        are not impacted.\n\n    Examples\n    --------\n    It is possible to mix sparse and dense arrays in the same run::\n\n      >>> X = np.array([[1., 0.], [2., 1.], [0., 0.]])\n      >>> y = np.array([0, 1, 2])\n\n      >>> from scipy.sparse import coo_matrix\n      >>> X_sparse = coo_matrix(X)\n\n      >>> from sklearn.utils import resample\n      >>> X, X_sparse, y = resample(X, X_sparse, y, random_state=0)\n      >>> X\n      array([[ 1.,  0.],\n             [ 2.,  1.],\n             [ 1.,  0.]])\n\n      >>> X_sparse                   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE\n      <3x2 sparse matrix of type '<... 'numpy.float64'>'\n          with 4 stored elements in Compressed Sparse Row format>\n\n      >>> X_sparse.toarray()\n      array([[ 1.,  0.],\n             [ 2.,  1.],\n             [ 1.,  0.]])\n\n      >>> y\n      array([0, 1, 0])\n\n      >>> resample(y, n_samples=2, random_state=0)\n      array([0, 1])\n\n\n    See also\n    --------\n    :func:`sklearn.utils.shuffle`\n    "
    random_state = check_random_state(options.pop('random_state', None))
    replace = options.pop('replace', True)
    max_n_samples = options.pop('n_samples', None)
    if options:
        raise ValueError(('Unexpected kw arguments: %r' % options.keys()))
    if (len(arrays) == 0):
        return None
    first = arrays[0]
    n_samples = (first.shape[0] if hasattr(first, 'shape') else len(first))
    if (max_n_samples is None):
        max_n_samples = n_samples
    elif ((max_n_samples > n_samples) and (not replace)):
        raise ValueError(('Cannot sample %d out of arrays with dim %d when replace is False' % (max_n_samples, n_samples)))
    check_consistent_length(*arrays)
    if replace:
        indices = random_state.randint(0, n_samples, size=(max_n_samples,))
    else:
        indices = np.arange(n_samples)
        random_state.shuffle(indices)
        indices = indices[:max_n_samples]
    arrays = [(a.tocsr() if issparse(a) else a) for a in arrays]
    resampled_arrays = [safe_indexing(a, indices) for a in arrays]
    if (len(resampled_arrays) == 1):
        return resampled_arrays[0]
    else:
        return resampled_arrays