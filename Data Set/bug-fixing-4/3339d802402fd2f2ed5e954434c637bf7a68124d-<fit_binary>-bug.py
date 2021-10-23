def fit_binary(est, i, X, y, alpha, C, learning_rate, max_iter, pos_weight, neg_weight, sample_weight, validation_mask=None, random_state=None):
    'Fit a single binary classifier.\n\n    The i\'th class is considered the "positive" class.\n\n    Parameters\n    ----------\n    est : Estimator object\n        The estimator to fit\n\n    i : int\n        Index of the positive class\n\n    X : numpy array or sparse matrix of shape [n_samples,n_features]\n        Training data\n\n    y : numpy array of shape [n_samples, ]\n        Target values\n\n    alpha : float\n        The regularization parameter\n\n    C : float\n        Maximum step size for passive aggressive\n\n    learning_rate : string\n        The learning rate. Accepted values are \'constant\', \'optimal\',\n        \'invscaling\', \'pa1\' and \'pa2\'.\n\n    max_iter : int\n        The maximum number of iterations (epochs)\n\n    pos_weight : float\n        The weight of the positive class\n\n    neg_weight : float\n        The weight of the negative class\n\n    sample_weight : numpy array of shape [n_samples, ]\n        The weight of each sample\n\n    validation_mask : numpy array of shape [n_samples, ] or None\n        Precomputed validation mask in case _fit_binary is called in the\n        context of a one-vs-rest reduction.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.\n    '
    (y_i, coef, intercept, average_coef, average_intercept) = _prepare_fit_binary(est, y, i)
    assert (y_i.shape[0] == y.shape[0] == sample_weight.shape[0])
    random_state = check_random_state(random_state)
    (dataset, intercept_decay) = make_dataset(X, y_i, sample_weight, random_state=random_state)
    penalty_type = est._get_penalty_type(est.penalty)
    learning_rate_type = est._get_learning_rate_type(learning_rate)
    if (validation_mask is None):
        validation_mask = est._make_validation_split(y_i)
    classes = np.array([(- 1), 1], dtype=y_i.dtype)
    validation_score_cb = est._make_validation_score_cb(validation_mask, X, y_i, sample_weight, classes=classes)
    seed = random_state.randint(MAX_INT)
    tol = (est.tol if (est.tol is not None) else (- np.inf))
    if (not est.average):
        result = plain_sgd(coef, intercept, est.loss_function_, penalty_type, alpha, C, est.l1_ratio, dataset, validation_mask, est.early_stopping, validation_score_cb, int(est.n_iter_no_change), max_iter, tol, int(est.fit_intercept), int(est.verbose), int(est.shuffle), seed, pos_weight, neg_weight, learning_rate_type, est.eta0, est.power_t, est.t_, intercept_decay)
    else:
        (standard_coef, standard_intercept, average_coef, average_intercept, n_iter_) = average_sgd(coef, intercept, average_coef, average_intercept, est.loss_function_, penalty_type, alpha, C, est.l1_ratio, dataset, validation_mask, est.early_stopping, validation_score_cb, int(est.n_iter_no_change), max_iter, tol, int(est.fit_intercept), int(est.verbose), int(est.shuffle), seed, pos_weight, neg_weight, learning_rate_type, est.eta0, est.power_t, est.t_, intercept_decay, est.average)
        if (len(est.classes_) == 2):
            est.average_intercept_[0] = average_intercept
        else:
            est.average_intercept_[i] = average_intercept
        result = (standard_coef, standard_intercept, n_iter_)
    return result