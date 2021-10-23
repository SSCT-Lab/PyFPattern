def test_spearmanr():
    x1 = [1, 2, 3, 4, 5]
    x2 = [5, 6, 7, 8, 7]
    expected = (0.8207826816681233, 0.0885870053135438)
    res = stats.spearmanr(x1, x2)
    assert_approx_equal(res[0], expected[0])
    assert_approx_equal(res[1], expected[1])
    attributes = ('correlation', 'pvalue')
    res = stats.spearmanr(x1, x2)
    check_named_results(res, attributes)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        assert_equal(stats.spearmanr([2, 2, 2], [2, 2, 2]), (np.nan, np.nan))
        assert_equal(stats.spearmanr([2, 0, 2], [2, 2, 2]), (np.nan, np.nan))
        assert_equal(stats.spearmanr([2, 2, 2], [2, 0, 2]), (np.nan, np.nan))
    assert_equal(stats.spearmanr([], []), (np.nan, np.nan))
    np.random.seed(7546)
    x = np.array([np.random.normal(loc=1, scale=1, size=500), np.random.normal(loc=1, scale=1, size=500)])
    corr = [[1.0, 0.3], [0.3, 1.0]]
    x = np.dot(np.linalg.cholesky(corr), x)
    expected = (0.28659685838743354, 6.579862219051161e-11)
    res = stats.spearmanr(x[0], x[1])
    assert_approx_equal(res[0], expected[0])
    assert_approx_equal(res[1], expected[1])
    assert_approx_equal(stats.spearmanr([1, 1, 2], [1, 1, 2])[0], 1.0)
    x = np.arange(10.0)
    x[9] = np.nan
    assert_array_equal(stats.spearmanr(x, x), (np.nan, np.nan))
    assert_allclose(stats.spearmanr(x, x, nan_policy='omit'), (1.0, 0))
    assert_raises(ValueError, stats.spearmanr, x, x, nan_policy='raise')
    assert_raises(ValueError, stats.spearmanr, x, x, nan_policy='foobar')
    x = np.arange(10.0)
    y = np.arange(20.0)
    assert_raises(ValueError, stats.spearmanr, x, y)
    x1 = [1, 2, 3, 4]
    x2 = [8, 7, 6, np.nan]
    res1 = stats.spearmanr(x1, x2, nan_policy='omit')
    res2 = stats.spearmanr(x1[:3], x2[:3], nan_policy='omit')
    assert_equal(res1, res2)