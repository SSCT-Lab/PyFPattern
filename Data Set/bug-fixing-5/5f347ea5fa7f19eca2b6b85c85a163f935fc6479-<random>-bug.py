def random(m, n, density=0.01, format='coo', dtype=None, random_state=None, data_rvs=None):
    'Generate a sparse matrix of the given shape and density with randomly\n    distributed values.\n\n    Parameters\n    ----------\n    m, n : int\n        shape of the matrix\n    density : real, optional\n        density of the generated matrix: density equal to one means a full\n        matrix, density of 0 means a matrix with no non-zero items.\n    format : str, optional\n        sparse matrix format.\n    dtype : dtype, optional\n        type of the returned matrix values.\n    random_state : {numpy.random.RandomState, int}, optional\n        Random number generator or random seed. If not given, the singleton\n        numpy.random will be used.  This random state will be used\n        for sampling the sparsity structure, but not necessarily for sampling\n        the values of the structurally nonzero entries of the matrix.\n    data_rvs : callable, optional\n        Samples a requested number of random values.\n        This function should take a single argument specifying the length\n        of the ndarray that it will return.  The structurally nonzero entries\n        of the sparse random matrix will be taken from the array sampled\n        by this function.  By default, uniform [0, 1) random values will be\n        sampled using the same random state as is used for sampling\n        the sparsity structure.\n\n    Returns\n    -------\n    res : sparse matrix\n\n    Examples\n    --------\n    >>> from scipy.sparse import random\n    >>> from scipy import stats\n    >>> class CustomRandomState(object):\n    ...     def randint(self, k):\n    ...         i = np.random.randint(k)\n    ...         return i - i % 2\n    >>> rs = CustomRandomState()\n    >>> rvs = stats.poisson(25, loc=10).rvs\n    >>> S = random(3, 4, density=0.25, random_state=rs, data_rvs=rvs)\n    >>> S.A\n    array([[ 36.,   0.,  33.,   0.],   # random\n           [  0.,   0.,   0.,   0.],\n           [  0.,   0.,  36.,   0.]])\n\n    Notes\n    -----\n    Only float types are supported for now.\n    '
    if ((density < 0) or (density > 1)):
        raise ValueError('density expected to be 0 <= density <= 1')
    dtype = np.dtype(dtype)
    if (dtype.char not in 'fdg'):
        raise NotImplementedError(('type %s not supported' % dtype))
    mn = (m * n)
    tp = np.intc
    if (mn > np.iinfo(tp).max):
        tp = np.int64
    if (mn > np.iinfo(tp).max):
        msg = 'Trying to generate a random sparse matrix such as the product of dimensions is\ngreater than %d - this is not supported on this machine\n'
        raise ValueError((msg % np.iinfo(tp).max))
    k = int(((density * m) * n))
    if (random_state is None):
        random_state = np.random
    elif isinstance(random_state, (int, np.integer)):
        random_state = np.random.RandomState(random_state)
    if (data_rvs is None):
        data_rvs = random_state.rand
    if (mn < (3 * k)):
        ind = random_state.choice(mn, size=k, replace=False)
    else:
        ind = np.empty(k, dtype=tp)
        selected = set()
        for i in xrange(k):
            j = random_state.randint(mn)
            while (j in selected):
                j = random_state.randint(mn)
            selected.add(j)
            ind[i] = j
    j = np.floor(((ind * 1.0) / m)).astype(tp)
    i = (ind - (j * m)).astype(tp)
    vals = data_rvs(k).astype(dtype)
    return coo_matrix((vals, (i, j)), shape=(m, n)).asformat(format)