def test_partial_fit_classes_error():
    X = [[3, 2]]
    y = [0]
    clf = MLPClassifier(solver='sgd')
    clf.partial_fit(X, y, classes=[0, 1])
    with pytest.raises(ValueError):
        clf.partial_fit(X, y, classes=[1, 2])