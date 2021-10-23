@ignore_warnings
def test_cross_validator_with_default_params():
    n_samples = 4
    n_unique_groups = 4
    n_splits = 2
    p = 2
    n_shuffle_splits = 10
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    X_1d = np.array([1, 2, 3, 4])
    y = np.array([1, 1, 2, 2])
    groups = np.array([1, 2, 3, 4])
    loo = LeaveOneOut()
    lpo = LeavePOut(p)
    kf = KFold(n_splits)
    skf = StratifiedKFold(n_splits)
    lolo = LeaveOneGroupOut()
    lopo = LeavePGroupsOut(p)
    ss = ShuffleSplit(random_state=0)
    ps = PredefinedSplit([1, 1, 2, 2])
    loo_repr = 'LeaveOneOut()'
    lpo_repr = 'LeavePOut(p=2)'
    kf_repr = 'KFold(n_splits=2, random_state=None, shuffle=False)'
    skf_repr = 'StratifiedKFold(n_splits=2, random_state=None, shuffle=False)'
    lolo_repr = 'LeaveOneGroupOut()'
    lopo_repr = 'LeavePGroupsOut(n_groups=2)'
    ss_repr = 'ShuffleSplit(n_splits=10, random_state=0, test_size=None, train_size=None)'
    ps_repr = 'PredefinedSplit(test_fold=array([1, 1, 2, 2]))'
    n_splits_expected = [n_samples, comb(n_samples, p), n_splits, n_splits, n_unique_groups, comb(n_unique_groups, p), n_shuffle_splits, 2]
    for (i, (cv, cv_repr)) in enumerate(zip([loo, lpo, kf, skf, lolo, lopo, ss, ps], [loo_repr, lpo_repr, kf_repr, skf_repr, lolo_repr, lopo_repr, ss_repr, ps_repr])):
        assert (n_splits_expected[i] == cv.get_n_splits(X, y, groups))
        np.testing.assert_equal(list(cv.split(X, y, groups)), list(cv.split(X_1d, y, groups)))
        for (train, test) in cv.split(X, y, groups):
            assert (np.asarray(train).dtype.kind == 'i')
            assert (np.asarray(test).dtype.kind == 'i')
        assert (cv_repr == repr(cv))
    msg = "The 'X' parameter should not be None."
    assert_raise_message(ValueError, msg, loo.get_n_splits, None, y, groups)
    assert_raise_message(ValueError, msg, lpo.get_n_splits, None, y, groups)