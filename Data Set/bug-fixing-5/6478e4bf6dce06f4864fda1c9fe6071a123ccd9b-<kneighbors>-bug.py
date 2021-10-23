def kneighbors(self, X=None, n_neighbors=None, return_distance=True):
    "Finds the K-neighbors of a point.\n        Returns indices of and distances to the neighbors of each point.\n\n        Parameters\n        ----------\n        X : array-like, shape (n_queries, n_features),                 or (n_queries, n_indexed) if metric == 'precomputed'\n            The query point or points.\n            If not provided, neighbors of each indexed point are returned.\n            In this case, the query point is not considered its own neighbor.\n\n        n_neighbors : int\n            Number of neighbors to get (default is the value\n            passed to the constructor).\n\n        return_distance : boolean, optional. Defaults to True.\n            If False, distances will not be returned\n\n        Returns\n        -------\n        neigh_dist : array, shape (n_queries, n_neighbors)\n            Array representing the lengths to points, only present if\n            return_distance=True\n\n        neigh_ind : array, shape (n_queries, n_neighbors)\n            Indices of the nearest points in the population matrix.\n\n        Examples\n        --------\n        In the following example, we construct a NeighborsClassifier\n        class from an array representing our data set and ask who's\n        the closest point to [1,1,1]\n\n        >>> samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]\n        >>> from sklearn.neighbors import NearestNeighbors\n        >>> neigh = NearestNeighbors(n_neighbors=1)\n        >>> neigh.fit(samples)\n        NearestNeighbors(n_neighbors=1)\n        >>> print(neigh.kneighbors([[1., 1., 1.]]))\n        (array([[0.5]]), array([[2]]))\n\n        As you can see, it returns [[0.5]], and [[2]], which means that the\n        element is at distance 0.5 and is the third element of samples\n        (indexes start at 0). You can also query for multiple points:\n\n        >>> X = [[0., 1., 0.], [1., 0., 1.]]\n        >>> neigh.kneighbors(X, return_distance=False)\n        array([[1],\n               [2]]...)\n\n        "
    check_is_fitted(self)
    if (n_neighbors is None):
        n_neighbors = self.n_neighbors
    elif (n_neighbors <= 0):
        raise ValueError(('Expected n_neighbors > 0. Got %d' % n_neighbors))
    elif (not isinstance(n_neighbors, numbers.Integral)):
        raise TypeError(('n_neighbors does not take %s value, enter integer value' % type(n_neighbors)))
    if (X is not None):
        query_is_train = False
        if (self.effective_metric_ == 'precomputed'):
            X = _check_precomputed(X)
        else:
            X = check_array(X, accept_sparse='csr')
    else:
        query_is_train = True
        X = self._fit_X
        n_neighbors += 1
    n_samples_fit = self.n_samples_fit_
    if (n_neighbors > n_samples_fit):
        raise ValueError(('Expected n_neighbors <= n_samples,  but n_samples = %d, n_neighbors = %d' % (n_samples_fit, n_neighbors)))
    n_jobs = effective_n_jobs(self.n_jobs)
    chunked_results = None
    if ((self._fit_method == 'brute') and (self.effective_metric_ == 'precomputed') and issparse(X)):
        results = _kneighbors_from_graph(X, n_neighbors=n_neighbors, return_distance=return_distance)
    elif (self._fit_method == 'brute'):
        reduce_func = partial(self._kneighbors_reduce_func, n_neighbors=n_neighbors, return_distance=return_distance)
        if (self.effective_metric_ == 'euclidean'):
            kwds = {
                'squared': True,
            }
        else:
            kwds = self.effective_metric_params_
        chunked_results = list(pairwise_distances_chunked(X, self._fit_X, reduce_func=reduce_func, metric=self.effective_metric_, n_jobs=n_jobs, **kwds))
    elif (self._fit_method in ['ball_tree', 'kd_tree']):
        if issparse(X):
            raise ValueError(("%s does not work with sparse matrices. Densify the data, or set algorithm='brute'" % self._fit_method))
        old_joblib = (LooseVersion(joblib.__version__) < LooseVersion('0.12'))
        if old_joblib:
            check_pickle = (False if old_joblib else None)
            delayed_query = delayed(_tree_query_parallel_helper, check_pickle=check_pickle)
            parallel_kwargs = {
                'backend': 'threading',
            }
        else:
            delayed_query = delayed(_tree_query_parallel_helper)
            parallel_kwargs = {
                'prefer': 'threads',
            }
        chunked_results = Parallel(n_jobs, **parallel_kwargs)((delayed_query(self._tree, X[s], n_neighbors, return_distance) for s in gen_even_slices(X.shape[0], n_jobs)))
    else:
        raise ValueError('internal: _fit_method not recognized')
    if (chunked_results is not None):
        if return_distance:
            (neigh_dist, neigh_ind) = zip(*chunked_results)
            results = (np.vstack(neigh_dist), np.vstack(neigh_ind))
        else:
            results = np.vstack(chunked_results)
    if (not query_is_train):
        return results
    else:
        if return_distance:
            (neigh_dist, neigh_ind) = results
        else:
            neigh_ind = results
        (n_queries, _) = X.shape
        sample_range = np.arange(n_queries)[:, None]
        sample_mask = (neigh_ind != sample_range)
        dup_gr_nbrs = np.all(sample_mask, axis=1)
        sample_mask[:, 0][dup_gr_nbrs] = False
        neigh_ind = np.reshape(neigh_ind[sample_mask], (n_queries, (n_neighbors - 1)))
        if return_distance:
            neigh_dist = np.reshape(neigh_dist[sample_mask], (n_queries, (n_neighbors - 1)))
            return (neigh_dist, neigh_ind)
        return neigh_ind