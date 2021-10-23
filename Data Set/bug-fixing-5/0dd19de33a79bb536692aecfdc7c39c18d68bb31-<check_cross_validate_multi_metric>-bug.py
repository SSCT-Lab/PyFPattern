def check_cross_validate_multi_metric(clf, X, y, scores):
    (train_mse_scores, test_mse_scores, train_r2_scores, test_r2_scores) = scores
    all_scoring = (('r2', 'neg_mean_squared_error'), {
        'r2': make_scorer(r2_score),
        'neg_mean_squared_error': 'neg_mean_squared_error',
    })
    keys_sans_train = set(('test_r2', 'test_neg_mean_squared_error', 'fit_time', 'score_time'))
    keys_with_train = keys_sans_train.union(set(('train_r2', 'train_neg_mean_squared_error')))
    for return_train_score in (True, False):
        for scoring in all_scoring:
            if return_train_score:
                cv_results = cross_validate(clf, X, y, cv=5, scoring=scoring)
                assert_array_almost_equal(cv_results['train_r2'], train_r2_scores)
                assert_array_almost_equal(cv_results['train_neg_mean_squared_error'], train_mse_scores)
            else:
                cv_results = cross_validate(clf, X, y, cv=5, scoring=scoring, return_train_score=False)
            assert_true(isinstance(cv_results, dict))
            assert_equal(set(cv_results.keys()), (keys_with_train if return_train_score else keys_sans_train))
            assert_array_almost_equal(cv_results['test_r2'], test_r2_scores)
            assert_array_almost_equal(cv_results['test_neg_mean_squared_error'], test_mse_scores)
            assert (type(cv_results['test_r2']) == np.ndarray)
            assert (type(cv_results['test_neg_mean_squared_error']) == np.ndarray)
            assert type((cv_results['fit_time'] == np.ndarray))
            assert type((cv_results['score_time'] == np.ndarray))
            assert np.all((cv_results['fit_time'] >= 0))
            assert np.all((cv_results['fit_time'] < 10))
            assert np.all((cv_results['score_time'] >= 0))
            assert np.all((cv_results['score_time'] < 10))