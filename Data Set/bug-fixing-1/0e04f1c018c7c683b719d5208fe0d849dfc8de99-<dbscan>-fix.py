

def dbscan(X, eps=0.5, min_samples=5, metric='minkowski', metric_params=None, algorithm='auto', leaf_size=30, p=2, sample_weight=None, n_jobs=1):
    'Perform DBSCAN clustering from vector array or distance matrix.\n\n    Read more in the :ref:`User Guide <dbscan>`.\n\n    Parameters\n    ----------\n    X : array or sparse (CSR) matrix of shape (n_samples, n_features), or             array of shape (n_samples, n_samples)\n        A feature array, or array of distances between samples if\n        ``metric=\'precomputed\'``.\n\n    eps : float, optional\n        The maximum distance between two samples for them to be considered\n        as in the same neighborhood.\n\n    min_samples : int, optional\n        The number of samples (or total weight) in a neighborhood for a point\n        to be considered as a core point. This includes the point itself.\n\n    metric : string, or callable\n        The metric to use when calculating distance between instances in a\n        feature array. If metric is a string or callable, it must be one of\n        the options allowed by :func:`sklearn.metrics.pairwise_distances` for\n        its metric parameter.\n        If metric is "precomputed", X is assumed to be a distance matrix and\n        must be square. X may be a sparse matrix, in which case only "nonzero"\n        elements may be considered neighbors for DBSCAN.\n\n    metric_params : dict, optional\n        Additional keyword arguments for the metric function.\n\n        .. versionadded:: 0.19\n\n    algorithm : {\'auto\', \'ball_tree\', \'kd_tree\', \'brute\'}, optional\n        The algorithm to be used by the NearestNeighbors module\n        to compute pointwise distances and find nearest neighbors.\n        See NearestNeighbors module documentation for details.\n\n    leaf_size : int, optional (default = 30)\n        Leaf size passed to BallTree or cKDTree. This can affect the speed\n        of the construction and query, as well as the memory required\n        to store the tree. The optimal value depends\n        on the nature of the problem.\n\n    p : float, optional\n        The power of the Minkowski metric to be used to calculate distance\n        between points.\n\n    sample_weight : array, shape (n_samples,), optional\n        Weight of each sample, such that a sample with a weight of at least\n        ``min_samples`` is by itself a core sample; a sample with negative\n        weight may inhibit its eps-neighbor from being core.\n        Note that weights are absolute, and default to 1.\n\n    n_jobs : int, optional (default = 1)\n        The number of parallel jobs to run for neighbors search.\n        If ``-1``, then the number of jobs is set to the number of CPU cores.\n\n    Returns\n    -------\n    core_samples : array [n_core_samples]\n        Indices of core samples.\n\n    labels : array [n_samples]\n        Cluster labels for each point.  Noisy samples are given the label -1.\n\n    Notes\n    -----\n    For an example, see :ref:`examples/cluster/plot_dbscan.py\n    <sphx_glr_auto_examples_cluster_plot_dbscan.py>`.\n\n    This implementation bulk-computes all neighborhood queries, which increases\n    the memory complexity to O(n.d) where d is the average number of neighbors,\n    while original DBSCAN had memory complexity O(n).\n\n    Sparse neighborhoods can be precomputed using\n    :func:`NearestNeighbors.radius_neighbors_graph\n    <sklearn.neighbors.NearestNeighbors.radius_neighbors_graph>`\n    with ``mode=\'distance\'``.\n\n    References\n    ----------\n    Ester, M., H. P. Kriegel, J. Sander, and X. Xu, "A Density-Based\n    Algorithm for Discovering Clusters in Large Spatial Databases with Noise".\n    In: Proceedings of the 2nd International Conference on Knowledge Discovery\n    and Data Mining, Portland, OR, AAAI Press, pp. 226-231. 1996\n    '
    if (not (eps > 0.0)):
        raise ValueError('eps must be positive.')
    X = check_array(X, accept_sparse='csr')
    if (sample_weight is not None):
        sample_weight = np.asarray(sample_weight)
        check_consistent_length(X, sample_weight)
    if ((metric == 'precomputed') and sparse.issparse(X)):
        neighborhoods = np.empty(X.shape[0], dtype=object)
        X.sum_duplicates()
        X_mask = (X.data <= eps)
        masked_indices = X.indices.astype(np.intp, copy=False)[X_mask]
        masked_indptr = np.concatenate(([0], np.cumsum(X_mask)))[X.indptr[1:]]
        masked_indices = np.insert(masked_indices, masked_indptr, np.arange(X.shape[0]))
        masked_indptr = (masked_indptr[:(- 1)] + np.arange(1, X.shape[0]))
        neighborhoods[:] = np.split(masked_indices, masked_indptr)
    else:
        neighbors_model = NearestNeighbors(radius=eps, algorithm=algorithm, leaf_size=leaf_size, metric=metric, metric_params=metric_params, p=p, n_jobs=n_jobs)
        neighbors_model.fit(X)
        neighborhoods = neighbors_model.radius_neighbors(X, eps, return_distance=False)
    if (sample_weight is None):
        n_neighbors = np.array([len(neighbors) for neighbors in neighborhoods])
    else:
        n_neighbors = np.array([np.sum(sample_weight[neighbors]) for neighbors in neighborhoods])
    labels = (- np.ones(X.shape[0], dtype=np.intp))
    core_samples = np.asarray((n_neighbors >= min_samples), dtype=np.uint8)
    dbscan_inner(core_samples, neighborhoods, labels)
    return (np.where(core_samples)[0], labels)
