@ignore_warnings(category=(DeprecationWarning, FutureWarning))
def check_regressors_train(name, regressor_orig):
    (X, y) = _boston_subset()
    y = StandardScaler().fit_transform(y.reshape((- 1), 1))
    y = y.ravel()
    regressor = clone(regressor_orig)
    y = multioutput_estimator_convert_y_2d(regressor, y)
    rnd = np.random.RandomState(0)
    if ((not hasattr(regressor, 'alphas')) and hasattr(regressor, 'alpha')):
        regressor.alpha = 0.01
    if (name == 'PassiveAggressiveRegressor'):
        regressor.C = 0.01
    with assert_raises(ValueError, msg='The classifer {} does not raise an error when incorrect/malformed input data for fit is passed. The number of training examples is not the same as the number of labels. Perhaps use check_X_y in fit.'.format(name)):
        regressor.fit(X, y[:(- 1)])
    if (name in CROSS_DECOMPOSITION):
        y_ = np.vstack([y, ((2 * y) + rnd.randint(2, size=len(y)))])
        y_ = y_.T
    else:
        y_ = y
    set_random_state(regressor)
    regressor.fit(X, y_)
    regressor.fit(X.tolist(), y_.tolist())
    y_pred = regressor.predict(X)
    assert_equal(y_pred.shape, y_.shape)
    if (name not in ('PLSCanonical', 'CCA', 'RANSACRegressor')):
        assert_greater(regressor.score(X, y_), 0.5)