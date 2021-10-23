def test_neighbors_accuracy_with_n_candidates():
    n_candidates_values = np.array([0.1, 50, 500])
    n_samples = 100
    n_features = 10
    n_iter = 10
    n_points = 5
    rng = np.random.RandomState(42)
    accuracies = np.zeros(n_candidates_values.shape[0], dtype=float)
    X = rng.rand(n_samples, n_features)
    for (i, n_candidates) in enumerate(n_candidates_values):
        lshf = ignore_warnings(LSHForest, category=DeprecationWarning)(n_candidates=n_candidates)
        ignore_warnings(lshf.fit)(X)
        for j in range(n_iter):
            query = X[rng.randint(0, n_samples)].reshape(1, (- 1))
            neighbors = lshf.kneighbors(query, n_neighbors=n_points, return_distance=False)
            distances = pairwise_distances(query, X, metric='cosine')
            ranks = np.argsort(distances)[0, :n_points]
            intersection = np.intersect1d(ranks, neighbors).shape[0]
            ratio = (intersection / float(n_points))
            accuracies[i] = (accuracies[i] + ratio)
        accuracies[i] = (accuracies[i] / float(n_iter))
    print('accuracies:', accuracies)
    assert_true(np.all((np.diff(accuracies) >= 0)), msg='Accuracies are not non-decreasing.')
    assert_true((np.ptp(accuracies) > 0), msg='Highest accuracy is not strictly greater than lowest.')