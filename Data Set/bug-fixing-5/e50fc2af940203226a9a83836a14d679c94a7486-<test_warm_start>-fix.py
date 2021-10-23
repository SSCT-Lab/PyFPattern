@pytest.mark.filterwarnings('ignore:.*did not converge.*')
@pytest.mark.parametrize('seed', (0, 1, 2))
def test_warm_start(seed):
    random_state = seed
    rng = np.random.RandomState(random_state)
    (n_samples, n_features, n_components) = (500, 2, 2)
    X = rng.rand(n_samples, n_features)
    g = GaussianMixture(n_components=n_components, n_init=1, max_iter=2, reg_covar=0, random_state=random_state, warm_start=False)
    h = GaussianMixture(n_components=n_components, n_init=1, max_iter=1, reg_covar=0, random_state=random_state, warm_start=True)
    g.fit(X)
    score1 = h.fit(X).score(X)
    score2 = h.fit(X).score(X)
    assert_almost_equal(g.weights_, h.weights_)
    assert_almost_equal(g.means_, h.means_)
    assert_almost_equal(g.precisions_, h.precisions_)
    assert (score2 > score1)
    g = GaussianMixture(n_components=n_components, n_init=1, max_iter=5, reg_covar=0, random_state=random_state, warm_start=False, tol=1e-06)
    h = GaussianMixture(n_components=n_components, n_init=1, max_iter=5, reg_covar=0, random_state=random_state, warm_start=True, tol=1e-06)
    g.fit(X)
    assert (not g.converged_)
    h.fit(X)
    for _ in range(1000):
        h.fit(X)
        if h.converged_:
            break
    assert h.converged_