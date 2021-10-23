def test_warm_start():
    random_state = 0
    rng = np.random.RandomState(random_state)
    (n_samples, n_features, n_components) = (500, 2, 2)
    X = rng.rand(n_samples, n_features)
    g = GaussianMixture(n_components=n_components, n_init=1, max_iter=2, reg_covar=0, random_state=random_state, warm_start=False)
    h = GaussianMixture(n_components=n_components, n_init=1, max_iter=1, reg_covar=0, random_state=random_state, warm_start=True)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', ConvergenceWarning)
        g.fit(X)
        score1 = h.fit(X).score(X)
        score2 = h.fit(X).score(X)
    assert_almost_equal(g.weights_, h.weights_)
    assert_almost_equal(g.means_, h.means_)
    assert_almost_equal(g.precisions_, h.precisions_)
    assert_greater(score2, score1)
    g = GaussianMixture(n_components=n_components, n_init=1, max_iter=5, reg_covar=0, random_state=random_state, warm_start=False, tol=1e-06)
    h = GaussianMixture(n_components=n_components, n_init=1, max_iter=5, reg_covar=0, random_state=random_state, warm_start=True, tol=1e-06)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', ConvergenceWarning)
        g.fit(X)
        h.fit(X).fit(X)
    assert_true((not g.converged_))
    assert_true(h.converged_)