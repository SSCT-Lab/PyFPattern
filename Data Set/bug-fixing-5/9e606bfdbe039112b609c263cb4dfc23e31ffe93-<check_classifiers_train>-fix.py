@ignore_warnings
def check_classifiers_train(name, classifier_orig):
    (X_m, y_m) = make_blobs(n_samples=300, random_state=0)
    (X_m, y_m) = shuffle(X_m, y_m, random_state=7)
    X_m = StandardScaler().fit_transform(X_m)
    y_b = y_m[(y_m != 2)]
    X_b = X_m[(y_m != 2)]
    for (X, y) in [(X_m, y_m), (X_b, y_b)]:
        classes = np.unique(y)
        n_classes = len(classes)
        (n_samples, n_features) = X.shape
        classifier = clone(classifier_orig)
        if (name in ['BernoulliNB', 'MultinomialNB', 'ComplementNB']):
            X -= X.min()
        set_random_state(classifier)
        with assert_raises(ValueError, msg='The classifer {} does not raise an error when incorrect/malformed input data for fit is passed. The number of training examples is not the same as the number of labels. Perhaps use check_X_y in fit.'.format(name)):
            classifier.fit(X, y[:(- 1)])
        classifier.fit(X, y)
        classifier.fit(X.tolist(), y.tolist())
        assert_true(hasattr(classifier, 'classes_'))
        y_pred = classifier.predict(X)
        assert_equal(y_pred.shape, (n_samples,))
        if (name not in ['BernoulliNB', 'MultinomialNB', 'ComplementNB']):
            assert_greater(accuracy_score(y, y_pred), 0.83)
        with assert_raises(ValueError, msg='The classifier {} does not raise an error when the number of features in predict is different from the number of features in fit.'.format(name)):
            classifier.predict(X.T)
        if hasattr(classifier, 'decision_function'):
            try:
                decision = classifier.decision_function(X)
                if (n_classes == 2):
                    assert_equal(decision.shape, (n_samples,))
                    dec_pred = (decision.ravel() > 0).astype(np.int)
                    assert_array_equal(dec_pred, y_pred)
                if ((n_classes == 3) and (not isinstance(classifier, BaseLibSVM))):
                    assert_equal(decision.shape, (n_samples, n_classes))
                    assert_array_equal(np.argmax(decision, axis=1), y_pred)
                with assert_raises(ValueError, msg='The classifier {} does not raise an error when the number of features in decision_function is different from the number of features in fit.'.format(name)):
                    classifier.decision_function(X.T)
            except NotImplementedError:
                pass
        if hasattr(classifier, 'predict_proba'):
            y_prob = classifier.predict_proba(X)
            assert_equal(y_prob.shape, (n_samples, n_classes))
            assert_array_equal(np.argmax(y_prob, axis=1), y_pred)
            assert_allclose(np.sum(y_prob, axis=1), np.ones(n_samples))
            with assert_raises(ValueError, msg='The classifier {} does not raise an error when the number of features in predict_proba is different from the number of features in fit.'.format(name)):
                classifier.predict_proba(X.T)
            if hasattr(classifier, 'predict_log_proba'):
                y_log_prob = classifier.predict_log_proba(X)
                assert_allclose(y_log_prob, np.log(y_prob), 8, atol=1e-09)
                assert_array_equal(np.argsort(y_log_prob), np.argsort(y_prob))