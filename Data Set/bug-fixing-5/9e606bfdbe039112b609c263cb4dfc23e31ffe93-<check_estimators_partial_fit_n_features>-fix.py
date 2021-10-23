@ignore_warnings(category=(DeprecationWarning, FutureWarning))
def check_estimators_partial_fit_n_features(name, estimator_orig):
    if (not hasattr(estimator_orig, 'partial_fit')):
        return
    estimator = clone(estimator_orig)
    (X, y) = make_blobs(n_samples=50, random_state=1)
    X -= X.min()
    try:
        if is_classifier(estimator):
            classes = np.unique(y)
            estimator.partial_fit(X, y, classes=classes)
        else:
            estimator.partial_fit(X, y)
    except NotImplementedError:
        return
    with assert_raises(ValueError, msg='The estimator {} does not raise an error when the number of features changes between calls to partial_fit.'.format(name)):
        estimator.partial_fit(X[:, :(- 1)], y)