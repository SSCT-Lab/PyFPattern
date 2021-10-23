

def trustworthiness(X, X_embedded, n_neighbors=5, precomputed=False):
    'Expresses to what extent the local structure is retained.\n\n    The trustworthiness is within [0, 1]. It is defined as\n\n    .. math::\n\n        T(k) = 1 - \x0crac{2}{nk (2n - 3k - 1)} \\sum^n_{i=1}\n            \\sum_{j \\in U^{(k)}_i} (r(i, j) - k)\n\n    where :math:`r(i, j)` is the rank of the embedded datapoint j\n    according to the pairwise distances between the embedded datapoints,\n    :math:`U^{(k)}_i` is the set of points that are in the k nearest\n    neighbors in the embedded space but not in the original space.\n\n    * "Neighborhood Preservation in Nonlinear Projection Methods: An\n      Experimental Study"\n      J. Venna, S. Kaski\n    * "Learning a Parametric Embedding by Preserving Local Structure"\n      L.J.P. van der Maaten\n\n    Parameters\n    ----------\n    X : array, shape (n_samples, n_features) or (n_samples, n_samples)\n        If the metric is \'precomputed\' X must be a square distance\n        matrix. Otherwise it contains a sample per row.\n\n    X_embedded : array, shape (n_samples, n_components)\n        Embedding of the training data in low-dimensional space.\n\n    n_neighbors : int, optional (default: 5)\n        Number of neighbors k that will be considered.\n\n    precomputed : bool, optional (default: False)\n        Set this flag if X is a precomputed square distance matrix.\n\n    Returns\n    -------\n    trustworthiness : float\n        Trustworthiness of the low-dimensional embedding.\n    '
    if precomputed:
        dist_X = X
    else:
        dist_X = pairwise_distances(X, squared=True)
    dist_X_embedded = pairwise_distances(X_embedded, squared=True)
    ind_X = np.argsort(dist_X, axis=1)
    ind_X_embedded = np.argsort(dist_X_embedded, axis=1)[:, 1:(n_neighbors + 1)]
    n_samples = X.shape[0]
    t = 0.0
    ranks = np.zeros(n_neighbors)
    for i in range(n_samples):
        for j in range(n_neighbors):
            ranks[j] = np.where((ind_X[i] == ind_X_embedded[(i, j)]))[0][0]
        ranks -= n_neighbors
        t += np.sum(ranks[(ranks > 0)])
    t = (1.0 - (t * (2.0 / ((n_samples * n_neighbors) * (((2.0 * n_samples) - (3.0 * n_neighbors)) - 1.0)))))
    return t
