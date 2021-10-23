def _k_init(X, n_clusters, x_squared_norms, random_state, n_local_trials=None):
    'Init n_clusters seeds according to k-means++\n\n    Parameters\n    ----------\n    X : array or sparse matrix, shape (n_samples, n_features)\n        The data to pick seeds for. To avoid memory copy, the input data\n        should be double precision (dtype=np.float64).\n\n    n_clusters : integer\n        The number of seeds to choose\n\n    x_squared_norms : array, shape (n_samples,)\n        Squared Euclidean norm of each data point.\n\n    random_state : int, RandomState instance\n        The generator used to initialize the centers. Use an int to make the\n        randomness deterministic.\n        See :term:`Glossary <random_state>`.\n\n    n_local_trials : integer, optional\n        The number of seeding trials for each center (except the first),\n        of which the one reducing inertia the most is greedily chosen.\n        Set to None to make the number of trials depend logarithmically\n        on the number of seeds (2+log(k)); this is the default.\n\n    Notes\n    -----\n    Selects initial cluster centers for k-mean clustering in a smart way\n    to speed up convergence. see: Arthur, D. and Vassilvitskii, S.\n    "k-means++: the advantages of careful seeding". ACM-SIAM symposium\n    on Discrete algorithms. 2007\n\n    Version ported from http://www.stanford.edu/~darthur/kMeansppTest.zip,\n    which is the implementation used in the aforementioned paper.\n    '
    (n_samples, n_features) = X.shape
    centers = np.empty((n_clusters, n_features), dtype=X.dtype)
    assert (x_squared_norms is not None), 'x_squared_norms None in _k_init'
    if (n_local_trials is None):
        n_local_trials = (2 + int(np.log(n_clusters)))
    center_id = random_state.randint(n_samples)
    if sp.issparse(X):
        centers[0] = X[center_id].toarray()
    else:
        centers[0] = X[center_id]
    closest_dist_sq = euclidean_distances(centers[(0, np.newaxis)], X, Y_norm_squared=x_squared_norms, squared=True)
    current_pot = closest_dist_sq.sum()
    for c in range(1, n_clusters):
        rand_vals = (random_state.random_sample(n_local_trials) * current_pot)
        candidate_ids = np.searchsorted(stable_cumsum(closest_dist_sq), rand_vals)
        np.clip(candidate_ids, None, (closest_dist_sq.size - 1), out=candidate_ids)
        distance_to_candidates = euclidean_distances(X[candidate_ids], X, Y_norm_squared=x_squared_norms, squared=True)
        best_candidate = None
        best_pot = None
        best_dist_sq = None
        for trial in range(n_local_trials):
            new_dist_sq = np.minimum(closest_dist_sq, distance_to_candidates[trial])
            new_pot = new_dist_sq.sum()
            if ((best_candidate is None) or (new_pot < best_pot)):
                best_candidate = candidate_ids[trial]
                best_pot = new_pot
                best_dist_sq = new_dist_sq
        if sp.issparse(X):
            centers[c] = X[best_candidate].toarray()
        else:
            centers[c] = X[best_candidate]
        current_pot = best_pot
        closest_dist_sq = best_dist_sq
    return centers