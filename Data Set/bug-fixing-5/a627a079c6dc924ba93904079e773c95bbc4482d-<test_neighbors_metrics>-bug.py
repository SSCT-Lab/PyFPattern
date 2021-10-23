def test_neighbors_metrics(n_samples=20, n_features=3, n_query_pts=2, n_neighbors=5):
    V = rng.rand(n_features, n_features)
    VI = np.dot(V, V.T)
    metrics = [('euclidean', {
        
    }), ('manhattan', {
        
    }), ('minkowski', dict(p=1)), ('minkowski', dict(p=2)), ('minkowski', dict(p=3)), ('minkowski', dict(p=np.inf)), ('chebyshev', {
        
    }), ('seuclidean', dict(V=rng.rand(n_features))), ('wminkowski', dict(p=3, w=rng.rand(n_features))), ('mahalanobis', dict(VI=VI))]
    algorithms = ['brute', 'ball_tree', 'kd_tree']
    X = rng.rand(n_samples, n_features)
    test = rng.rand(n_query_pts, n_features)
    for (metric, metric_params) in metrics:
        results = []
        p = metric_params.pop('p', 2)
        for algorithm in algorithms:
            if ((algorithm == 'kd_tree') and (metric not in neighbors.KDTree.valid_metrics)):
                assert_raises(ValueError, neighbors.NearestNeighbors, algorithm=algorithm, metric=metric, metric_params=metric_params)
                continue
            neigh = neighbors.NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm, metric=metric, p=p, metric_params=metric_params)
            neigh.fit(X)
            results.append(neigh.kneighbors(test, return_distance=True))
        assert_array_almost_equal(results[0][0], results[1][0])
        assert_array_almost_equal(results[0][1], results[1][1])