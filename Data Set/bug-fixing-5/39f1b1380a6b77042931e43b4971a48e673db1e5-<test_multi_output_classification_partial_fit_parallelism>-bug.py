def test_multi_output_classification_partial_fit_parallelism():
    sgd_linear_clf = SGDClassifier(loss='log', random_state=1, max_iter=5)
    mor = MultiOutputClassifier(sgd_linear_clf, n_jobs=(- 1))
    mor.partial_fit(X, y, classes)
    est1 = mor.estimators_[0]
    mor.partial_fit(X, y)
    est2 = mor.estimators_[0]
    assert_false((est1 is est2))