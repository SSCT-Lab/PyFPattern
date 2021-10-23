def test_fastica_simple(add_noise=False):
    rng = np.random.RandomState(0)
    n_samples = 1000
    s1 = (((2 * np.sin(np.linspace(0, 100, n_samples))) > 0) - 1)
    s2 = stats.t.rvs(1, size=n_samples)
    s = np.c_[(s1, s2)].T
    center_and_norm(s)
    (s1, s2) = s
    phi = 0.6
    mixing = np.array([[np.cos(phi), np.sin(phi)], [np.sin(phi), (- np.cos(phi))]])
    m = np.dot(mixing, s)
    if add_noise:
        m += (0.1 * rng.randn(2, 1000))
    center_and_norm(m)

    def g_test(x):
        return ((x ** 3), (3 * (x ** 2)).mean(axis=(- 1)))
    algos = ['parallel', 'deflation']
    nls = ['logcosh', 'exp', 'cube', g_test]
    whitening = [True, False]
    for (algo, nl, whiten) in itertools.product(algos, nls, whitening):
        if whiten:
            (k_, mixing_, s_) = fastica(m.T, fun=nl, algorithm=algo)
            assert_raises(ValueError, fastica, m.T, fun=np.tanh, algorithm=algo)
        else:
            X = PCA(n_components=2, whiten=True).fit_transform(m.T)
            (k_, mixing_, s_) = fastica(X, fun=nl, algorithm=algo, whiten=False)
            assert_raises(ValueError, fastica, X, fun=np.tanh, algorithm=algo)
        s_ = s_.T
        if whiten:
            assert_almost_equal(s_, np.dot(np.dot(mixing_, k_), m))
        center_and_norm(s_)
        (s1_, s2_) = s_
        if (abs(np.dot(s1_, s2)) > abs(np.dot(s1_, s1))):
            (s2_, s1_) = s_
        s1_ *= np.sign(np.dot(s1_, s1))
        s2_ *= np.sign(np.dot(s2_, s2))
        if (not add_noise):
            assert_almost_equal((np.dot(s1_, s1) / n_samples), 1, decimal=2)
            assert_almost_equal((np.dot(s2_, s2) / n_samples), 1, decimal=2)
        else:
            assert_almost_equal((np.dot(s1_, s1) / n_samples), 1, decimal=1)
            assert_almost_equal((np.dot(s2_, s2) / n_samples), 1, decimal=1)
    (_, _, sources_fun) = fastica(m.T, fun=nl, algorithm=algo, random_state=0)
    ica = FastICA(fun=nl, algorithm=algo, random_state=0)
    sources = ica.fit_transform(m.T)
    assert_equal(ica.components_.shape, (2, 2))
    assert_equal(sources.shape, (1000, 2))
    assert_array_almost_equal(sources_fun, sources)
    assert_array_almost_equal(sources, ica.transform(m.T))
    assert_equal(ica.mixing_.shape, (2, 2))
    for fn in [np.tanh, 'exp(-.5(x^2))']:
        ica = FastICA(fun=fn, algorithm=algo, random_state=0)
        assert_raises(ValueError, ica.fit, m.T)
    assert_raises(TypeError, FastICA(fun=range(10)).fit, m.T)