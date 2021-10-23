def test_sag_regressor():
    'tests if the sag regressor performs well'
    (xmin, xmax) = ((- 5), 5)
    n_samples = 20
    tol = 0.001
    max_iter = 50
    alpha = 0.1
    rng = np.random.RandomState(0)
    X = np.linspace(xmin, xmax, n_samples).reshape(n_samples, 1)
    y = (0.5 * X.ravel())
    clf1 = Ridge(tol=tol, solver='sag', max_iter=max_iter, alpha=(alpha * n_samples), random_state=rng)
    clf2 = clone(clf1)
    clf1.fit(X, y)
    clf2.fit(sp.csr_matrix(X), y)
    score1 = clf1.score(X, y)
    score2 = clf2.score(X, y)
    assert_greater(score1, 0.99)
    assert_greater(score2, 0.99)
    y = ((0.5 * X.ravel()) + rng.randn(n_samples, 1).ravel())
    clf1 = Ridge(tol=tol, solver='sag', max_iter=max_iter, alpha=(alpha * n_samples))
    clf2 = clone(clf1)
    clf1.fit(X, y)
    clf2.fit(sp.csr_matrix(X), y)
    score1 = clf1.score(X, y)
    score2 = clf2.score(X, y)
    score2 = clf2.score(X, y)
    assert_greater(score1, 0.5)
    assert_greater(score2, 0.5)