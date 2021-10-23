def fit(self, X, y=None, sample_weight=None):
    "Perform DBSCAN clustering from features, or distance matrix.\n\n        Parameters\n        ----------\n        X : array-like or sparse matrix, shape (n_samples, n_features), or             (n_samples, n_samples)\n            Training instances to cluster, or distances between instances if\n            ``metric='precomputed'``. If a sparse matrix is provided, it will\n            be converted into a sparse ``csr_matrix``.\n\n        sample_weight : array, shape (n_samples,), optional\n            Weight of each sample, such that a sample with a weight of at least\n            ``min_samples`` is by itself a core sample; a sample with a\n            negative weight may inhibit its eps-neighbor from being core.\n            Note that weights are absolute, and default to 1.\n\n        y : Ignored\n            Not used, present here for API consistency by convention.\n\n        Returns\n        -------\n        self\n\n        "
    X = check_array(X, accept_sparse='csr')
    if (not (self.eps > 0.0)):
        raise ValueError('eps must be positive.')
    if (sample_weight is not None):
        sample_weight = np.asarray(sample_weight)
        check_consistent_length(X, sample_weight)
    if ((self.metric == 'precomputed') and sparse.issparse(X)):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', sparse.SparseEfficiencyWarning)
            X.setdiag(X.diagonal())
    neighbors_model = NearestNeighbors(radius=self.eps, algorithm=self.algorithm, leaf_size=self.leaf_size, metric=self.metric, metric_params=self.metric_params, p=self.p, n_jobs=self.n_jobs)
    neighbors_model.fit(X)
    neighborhoods = neighbors_model.radius_neighbors(X, return_distance=False)
    if (sample_weight is None):
        n_neighbors = np.array([len(neighbors) for neighbors in neighborhoods])
    else:
        n_neighbors = np.array([np.sum(sample_weight[neighbors]) for neighbors in neighborhoods])
    labels = np.full(X.shape[0], (- 1), dtype=np.intp)
    core_samples = np.asarray((n_neighbors >= self.min_samples), dtype=np.uint8)
    dbscan_inner(core_samples, neighborhoods, labels)
    self.core_sample_indices_ = np.where(core_samples)[0]
    self.labels_ = labels
    if len(self.core_sample_indices_):
        self.components_ = X[self.core_sample_indices_].copy()
    else:
        self.components_ = np.empty((0, X.shape[1]))
    return self