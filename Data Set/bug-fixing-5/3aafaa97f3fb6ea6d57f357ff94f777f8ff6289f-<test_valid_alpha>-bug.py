def test_valid_alpha():
    n_classes = 2
    (X, y) = make_classification(n_classes=n_classes, n_samples=200, random_state=0)
    for alpha in [(- 0.1), 0, 1, 1.1, None]:
        assert_raises(ValueError, (lambda **kwargs: label_propagation.LabelSpreading(**kwargs).fit(X, y)), alpha=alpha)