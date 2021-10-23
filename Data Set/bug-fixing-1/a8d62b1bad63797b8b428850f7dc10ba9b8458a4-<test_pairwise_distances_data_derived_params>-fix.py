

@pytest.mark.parametrize('n_jobs', [1, 2])
@pytest.mark.parametrize('metric', ['seuclidean', 'mahalanobis'])
@pytest.mark.parametrize('dist_function', [pairwise_distances, pairwise_distances_chunked])
@pytest.mark.parametrize('y_is_x', [True, False], ids=['Y is X', 'Y is not X'])
def test_pairwise_distances_data_derived_params(n_jobs, metric, dist_function, y_is_x):
    with config_context(working_memory=1):
        rng = np.random.RandomState(0)
        X = rng.random_sample((1000, 10))
        if y_is_x:
            Y = X
            expected_dist_default_params = squareform(pdist(X, metric=metric))
            if (metric == 'seuclidean'):
                params = {
                    'V': np.var(X, axis=0, ddof=1),
                }
            else:
                params = {
                    'VI': np.linalg.inv(np.cov(X.T)).T,
                }
        else:
            Y = rng.random_sample((1000, 10))
            expected_dist_default_params = cdist(X, Y, metric=metric)
            if (metric == 'seuclidean'):
                params = {
                    'V': np.var(np.vstack([X, Y]), axis=0, ddof=1),
                }
            else:
                params = {
                    'VI': np.linalg.inv(np.cov(np.vstack([X, Y]).T)).T,
                }
        expected_dist_explicit_params = cdist(X, Y, metric=metric, **params)
        dist = np.vstack(tuple(dist_function(X, Y, metric=metric, n_jobs=n_jobs)))
        assert_allclose(dist, expected_dist_explicit_params)
        assert_allclose(dist, expected_dist_default_params)
