def get_results(dataset):
    (X_full, y_full) = (dataset.data, dataset.target)
    n_samples = X_full.shape[0]
    n_features = X_full.shape[1]
    full_scores = cross_val_score(REGRESSOR, X_full, y_full, scoring='neg_mean_squared_error', cv=N_SPLITS)
    missing_rate = 0.75
    n_missing_samples = int(np.floor((n_samples * missing_rate)))
    missing_samples = np.hstack((np.zeros((n_samples - n_missing_samples), dtype=np.bool), np.ones(n_missing_samples, dtype=np.bool)))
    rng.shuffle(missing_samples)
    missing_features = rng.randint(0, n_features, n_missing_samples)
    X_missing = X_full.copy()
    X_missing[(np.where(missing_samples)[0], missing_features)] = 0
    y_missing = y_full.copy()
    imputer = SimpleImputer(missing_values=0, strategy='constant', fill_value=0)
    zero_impute_scores = get_scores_for_imputer(imputer, X_missing, y_missing)
    imputer = SimpleImputer(missing_values=0, strategy='mean')
    mean_impute_scores = get_scores_for_imputer(imputer, X_missing, y_missing)
    imputer = IterativeImputer(missing_values=0, random_state=0, n_nearest_features=5)
    iterative_impute_scores = get_scores_for_imputer(imputer, X_missing, y_missing)
    return ((full_scores.mean(), full_scores.std()), (zero_impute_scores.mean(), zero_impute_scores.std()), (mean_impute_scores.mean(), mean_impute_scores.std()), (iterative_impute_scores.mean(), iterative_impute_scores.std()))