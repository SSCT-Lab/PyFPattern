

def learning_curve(estimator, X, y, groups=None, train_sizes=np.linspace(0.1, 1.0, 5), cv=None, scoring=None, exploit_incremental_learning=False, n_jobs=1, pre_dispatch='all', verbose=0, shuffle=False, random_state=None):
    'Learning curve.\n\n    Determines cross-validated training and test scores for different training\n    set sizes.\n\n    A cross-validation generator splits the whole dataset k times in training\n    and test data. Subsets of the training set with varying sizes will be used\n    to train the estimator and a score for each training subset size and the\n    test set will be computed. Afterwards, the scores will be averaged over\n    all k runs for each training subset size.\n\n    Read more in the :ref:`User Guide <learning_curve>`.\n\n    Parameters\n    ----------\n    estimator : object type that implements the "fit" and "predict" methods\n        An object of that type which is cloned for each validation.\n\n    X : array-like, shape (n_samples, n_features)\n        Training vector, where n_samples is the number of samples and\n        n_features is the number of features.\n\n    y : array-like, shape (n_samples) or (n_samples, n_features), optional\n        Target relative to X for classification or regression;\n        None for unsupervised learning.\n\n    groups : array-like, with shape (n_samples,), optional\n        Group labels for the samples used while splitting the dataset into\n        train/test set.\n\n    train_sizes : array-like, shape (n_ticks,), dtype float or int\n        Relative or absolute numbers of training examples that will be used to\n        generate the learning curve. If the dtype is float, it is regarded as a\n        fraction of the maximum size of the training set (that is determined\n        by the selected validation method), i.e. it has to be within (0, 1].\n        Otherwise it is interpreted as absolute sizes of the training sets.\n        Note that for classification the number of samples usually have to\n        be big enough to contain at least one sample from each class.\n        (default: np.linspace(0.1, 1.0, 5))\n\n    cv : int, cross-validation generator or an iterable, optional\n        Determines the cross-validation splitting strategy.\n        Possible inputs for cv are:\n\n        - None, to use the default 3-fold cross validation,\n        - integer, to specify the number of folds in a `(Stratified)KFold`,\n        - An object to be used as a cross-validation generator.\n        - An iterable yielding train, test splits.\n\n        For integer/None inputs, if the estimator is a classifier and ``y`` is\n        either binary or multiclass, :class:`StratifiedKFold` is used. In all\n        other cases, :class:`KFold` is used.\n\n        Refer :ref:`User Guide <cross_validation>` for the various\n        cross-validation strategies that can be used here.\n\n    scoring : string, callable or None, optional, default: None\n        A string (see model evaluation documentation) or\n        a scorer callable object / function with signature\n        ``scorer(estimator, X, y)``.\n\n    exploit_incremental_learning : boolean, optional, default: False\n        If the estimator supports incremental learning, this will be\n        used to speed up fitting for different training set sizes.\n\n    n_jobs : integer, optional\n        Number of jobs to run in parallel (default 1).\n\n    pre_dispatch : integer or string, optional\n        Number of predispatched jobs for parallel execution (default is\n        all). The option can reduce the allocated memory. The string can\n        be an expression like \'2*n_jobs\'.\n\n    verbose : integer, optional\n        Controls the verbosity: the higher, the more messages.\n\n    shuffle : boolean, optional\n        Whether to shuffle training data before taking prefixes of it\n        based on``train_sizes``.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`. Used when ``shuffle`` == \'True\'.\n\n    Returns\n    -------\n    train_sizes_abs : array, shape = (n_unique_ticks,), dtype int\n        Numbers of training examples that has been used to generate the\n        learning curve. Note that the number of ticks might be less\n        than n_ticks because duplicate entries will be removed.\n\n    train_scores : array, shape (n_ticks, n_cv_folds)\n        Scores on training sets.\n\n    test_scores : array, shape (n_ticks, n_cv_folds)\n        Scores on test set.\n\n    Notes\n    -----\n    See :ref:`examples/model_selection/plot_learning_curve.py\n    <sphx_glr_auto_examples_model_selection_plot_learning_curve.py>`\n    '
    if (exploit_incremental_learning and (not hasattr(estimator, 'partial_fit'))):
        raise ValueError('An estimator must support the partial_fit interface to exploit incremental learning')
    (X, y, groups) = indexable(X, y, groups)
    cv = check_cv(cv, y, classifier=is_classifier(estimator))
    cv_iter = list(cv.split(X, y, groups))
    scorer = check_scoring(estimator, scoring=scoring)
    n_max_training_samples = len(cv_iter[0][0])
    train_sizes_abs = _translate_train_sizes(train_sizes, n_max_training_samples)
    n_unique_ticks = train_sizes_abs.shape[0]
    if (verbose > 0):
        print(('[learning_curve] Training set sizes: ' + str(train_sizes_abs)))
    parallel = Parallel(n_jobs=n_jobs, pre_dispatch=pre_dispatch, verbose=verbose)
    if shuffle:
        rng = check_random_state(random_state)
        cv_iter = ((rng.permutation(train), test) for (train, test) in cv_iter)
    if exploit_incremental_learning:
        classes = (np.unique(y) if is_classifier(estimator) else None)
        out = parallel((delayed(_incremental_fit_estimator)(clone(estimator), X, y, classes, train, test, train_sizes_abs, scorer, verbose) for (train, test) in cv_iter))
    else:
        train_test_proportions = []
        for (train, test) in cv_iter:
            for n_train_samples in train_sizes_abs:
                train_test_proportions.append((train[:n_train_samples], test))
        out = parallel((delayed(_fit_and_score)(clone(estimator), X, y, scorer, train, test, verbose, parameters=None, fit_params=None, return_train_score=True) for (train, test) in train_test_proportions))
        out = np.array(out)
        n_cv_folds = (out.shape[0] // n_unique_ticks)
        out = out.reshape(n_cv_folds, n_unique_ticks, 2)
    out = np.asarray(out).transpose((2, 1, 0))
    return (train_sizes_abs, out[0], out[1])
