@pytest.mark.filterwarnings("ignore:The parameter 'iid' is deprecated")
def test_grid_search_cv_results():
    (X, y) = make_classification(n_samples=50, n_features=4, random_state=42)
    n_splits = 3
    n_grid_points = 6
    params = [dict(kernel=['rbf'], C=[1, 10], gamma=[0.1, 1]), dict(kernel=['poly'], degree=[1, 2])]
    param_keys = ('param_C', 'param_degree', 'param_gamma', 'param_kernel')
    score_keys = ('mean_test_score', 'mean_train_score', 'rank_test_score', 'split0_test_score', 'split1_test_score', 'split2_test_score', 'split0_train_score', 'split1_train_score', 'split2_train_score', 'std_test_score', 'std_train_score', 'mean_fit_time', 'std_fit_time', 'mean_score_time', 'std_score_time')
    n_candidates = n_grid_points
    for iid in (False, True):
        search = GridSearchCV(SVC(), cv=n_splits, iid=iid, param_grid=params, return_train_score=True)
        search.fit(X, y)
        assert (iid == search.iid)
        cv_results = search.cv_results_
        assert all((cv_results['rank_test_score'] >= 1))
        assert (all((cv_results[k] >= 0)) for k in score_keys if (k is not 'rank_test_score'))
        assert (all((cv_results[k] <= 1)) for k in score_keys if (('time' not in k) and (k is not 'rank_test_score')))
        check_cv_results_array_types(search, param_keys, score_keys)
        check_cv_results_keys(cv_results, param_keys, score_keys, n_candidates)
        cv_results = search.cv_results_
        n_candidates = len(search.cv_results_['params'])
        assert all(((cv_results['param_C'].mask[i] and cv_results['param_gamma'].mask[i] and (not cv_results['param_degree'].mask[i])) for i in range(n_candidates) if (cv_results['param_kernel'][i] == 'linear')))
        assert all((((not cv_results['param_C'].mask[i]) and (not cv_results['param_gamma'].mask[i]) and cv_results['param_degree'].mask[i]) for i in range(n_candidates) if (cv_results['param_kernel'][i] == 'rbf')))