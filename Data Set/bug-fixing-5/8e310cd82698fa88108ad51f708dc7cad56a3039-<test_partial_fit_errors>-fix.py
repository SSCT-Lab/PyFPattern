def test_partial_fit_errors():
    X = [[3, 2], [1, 6]]
    y = [1, 0]
    with pytest.raises(ValueError):
        MLPClassifier(solver='sgd').partial_fit(X, y, classes=[2])
    assert (not hasattr(MLPClassifier(solver='lbfgs'), 'partial_fit'))