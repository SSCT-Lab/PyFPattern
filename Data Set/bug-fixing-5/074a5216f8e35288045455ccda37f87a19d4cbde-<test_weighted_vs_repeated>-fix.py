def test_weighted_vs_repeated():
    rng = np.random.RandomState(0)
    sample_weight = rng.randint(1, 5, size=n_samples)
    X_repeat = np.repeat(X, sample_weight, axis=0)
    estimators = [KMeans(init='k-means++', n_clusters=n_clusters, random_state=42), KMeans(init='random', n_clusters=n_clusters, random_state=42), KMeans(init=centers.copy(), n_clusters=n_clusters, random_state=42), MiniBatchKMeans(n_clusters=n_clusters, batch_size=10, random_state=42)]
    for estimator in estimators:
        est_weighted = clone(estimator).fit(X, sample_weight=sample_weight)
        est_repeated = clone(estimator).fit(X_repeat)
        repeated_labels = np.repeat(est_weighted.labels_, sample_weight)
        assert_almost_equal(v_measure_score(est_repeated.labels_, repeated_labels), 1.0)
        if (not isinstance(estimator, MiniBatchKMeans)):
            assert_almost_equal(_sort_centers(est_weighted.cluster_centers_), _sort_centers(est_repeated.cluster_centers_))