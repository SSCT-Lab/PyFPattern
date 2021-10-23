@ignore_warnings(category=(DeprecationWarning, FutureWarning))
def check_estimators_empty_data_messages(name, estimator_orig):
    e = clone(estimator_orig)
    set_random_state(e, 1)
    X_zero_samples = np.empty(0).reshape(0, 3)
    assert_raises(ValueError, e.fit, X_zero_samples, [])
    X_zero_features = np.empty(0).reshape(3, 0)
    y = multioutput_estimator_convert_y_2d(e, np.array([1, 0, 1]))
    msg = '0 feature\\(s\\) \\(shape=\\(3, 0\\)\\) while a minimum of \\d* is required.'
    assert_raises_regex(ValueError, msg, e.fit, X_zero_features, y)