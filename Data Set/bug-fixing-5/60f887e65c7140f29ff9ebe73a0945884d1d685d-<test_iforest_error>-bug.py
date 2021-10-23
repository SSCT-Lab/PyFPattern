def test_iforest_error():
    'Test that it gives proper exception on deficient input.'
    X = iris.data
    assert_raises(ValueError, IsolationForest(max_samples=(- 1)).fit, X)
    assert_raises(ValueError, IsolationForest(max_samples=0.0).fit, X)
    assert_raises(ValueError, IsolationForest(max_samples=2.0).fit, X)
    assert_warns_message(UserWarning, 'max_samples will be set to n_samples for estimation', IsolationForest(max_samples=1000).fit, X)
    assert_no_warnings(IsolationForest(max_samples='auto').fit, X)
    assert_no_warnings(IsolationForest(max_samples=np.int64(2)).fit, X)
    assert_raises(ValueError, IsolationForest(max_samples='foobar').fit, X)
    assert_raises(ValueError, IsolationForest(max_samples=1.5).fit, X)
    assert_raises(ValueError, IsolationForest().fit(X).predict, X[:, 1:])