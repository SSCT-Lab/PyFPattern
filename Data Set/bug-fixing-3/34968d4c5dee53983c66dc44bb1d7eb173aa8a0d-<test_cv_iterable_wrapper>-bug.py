def test_cv_iterable_wrapper():
    y_multiclass = np.array([0, 1, 0, 1, 2, 1, 2, 0, 2])
    with warnings.catch_warnings(record=True):
        from sklearn.cross_validation import StratifiedKFold as OldSKF
    cv = OldSKF(y_multiclass, n_folds=3)
    wrapped_old_skf = _CVIterableWrapper(cv)
    np.testing.assert_equal(list(cv), list(wrapped_old_skf.split()))
    assert_equal(len(cv), wrapped_old_skf.get_n_splits())
    kf_iter = KFold(n_splits=5).split(X, y)
    kf_iter_wrapped = check_cv(kf_iter)
    assert_array_equal(list(kf_iter_wrapped.split(X, y)), list(kf_iter_wrapped.split(X, y)))
    kf_randomized_iter = KFold(n_splits=5, shuffle=True).split(X, y)
    kf_randomized_iter_wrapped = check_cv(kf_randomized_iter)
    assert_array_equal(list(kf_randomized_iter_wrapped.split(X, y)), list(kf_randomized_iter_wrapped.split(X, y)))
    assert_true(np.any((np.array(list(kf_iter_wrapped.split(X, y))) != np.array(list(kf_randomized_iter_wrapped.split(X, y))))))