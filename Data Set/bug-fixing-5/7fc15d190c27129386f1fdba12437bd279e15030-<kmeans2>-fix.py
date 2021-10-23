def kmeans2(data, k, iter=10, thresh=1e-05, minit='random', missing='warn', check_finite=True):
    "\n    Classify a set of observations into k clusters using the k-means algorithm.\n\n    The algorithm attempts to minimize the Euclidian distance between\n    observations and centroids. Several initialization methods are\n    included.\n\n    Parameters\n    ----------\n    data : ndarray\n        A 'M' by 'N' array of 'M' observations in 'N' dimensions or a length\n        'M' array of 'M' one-dimensional observations.\n    k : int or ndarray\n        The number of clusters to form as well as the number of\n        centroids to generate. If `minit` initialization string is\n        'matrix', or if a ndarray is given instead, it is\n        interpreted as initial cluster to use instead.\n    iter : int, optional\n        Number of iterations of the k-means algorithm to run. Note\n        that this differs in meaning from the iters parameter to\n        the kmeans function.\n    thresh : float, optional\n        (not used yet)\n    minit : str, optional\n        Method for initialization. Available methods are 'random',\n        'points', and 'matrix':\n\n        'random': generate k centroids from a Gaussian with mean and\n        variance estimated from the data.\n\n        'points': choose k observations (rows) at random from data for\n        the initial centroids.\n\n        'matrix': interpret the k parameter as a k by M (or length k\n        array for one-dimensional data) array of initial centroids.\n    missing : str, optional\n        Method to deal with empty clusters. Available methods are\n        'warn' and 'raise':\n\n        'warn': give a warning and continue.\n\n        'raise': raise an ClusterError and terminate the algorithm.\n    check_finite : bool, optional\n        Whether to check that the input matrices contain only finite numbers.\n        Disabling may give a performance gain, but may result in problems\n        (crashes, non-termination) if the inputs do contain infinities or NaNs.\n        Default: True\n\n    Returns\n    -------\n    centroid : ndarray\n        A 'k' by 'N' array of centroids found at the last iteration of\n        k-means.\n    label : ndarray\n        label[i] is the code or index of the centroid the\n        i'th observation is closest to.\n\n    "
    data = _asarray_validated(data, check_finite=check_finite)
    if (missing not in _valid_miss_meth):
        raise ValueError(('Unkown missing method: %s' % str(missing)))
    nd = np.ndim(data)
    if (nd == 1):
        d = 1
    elif (nd == 2):
        d = data.shape[1]
    else:
        raise ValueError('Input of rank > 2 not supported')
    if (np.size(data) < 1):
        raise ValueError('Input has 0 items.')
    if ((np.size(k) > 1) or (minit == 'matrix')):
        if (not (nd == np.ndim(k))):
            raise ValueError('k is not an int and has not same rank than data')
        if (d == 1):
            nc = len(k)
        else:
            (nc, dc) = k.shape
            if (not (dc == d)):
                raise ValueError('k is not an int and has not same rank than                        data')
        clusters = k.copy()
    else:
        try:
            nc = int(k)
        except TypeError:
            raise ValueError(('k (%s) could not be converted to an integer ' % str(k)))
        if (nc < 1):
            raise ValueError(('kmeans2 for 0 clusters ? (k was %s)' % str(k)))
        if (not (nc == k)):
            warnings.warn('k was not an integer, was converted.')
        try:
            init = _valid_init_meth[minit]
        except KeyError:
            raise ValueError(('unknown init method %s' % str(minit)))
        clusters = init(data, k)
    if (int(iter) < 1):
        raise ValueError(('iter = %s is not valid.  iter must be a positive integer.' % iter))
    return _kmeans2(data, clusters, iter, nc, _valid_miss_meth[missing])