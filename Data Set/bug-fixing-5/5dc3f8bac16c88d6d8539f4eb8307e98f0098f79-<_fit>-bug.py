def _fit(self, X, y, max_samples=None, max_depth=None, sample_weight=None):
    'Build a Bagging ensemble of estimators from the training\n           set (X, y).\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix} of shape (n_samples, n_features)\n            The training input samples. Sparse matrices are accepted only if\n            they are supported by the base estimator.\n\n        y : array-like of shape (n_samples,)\n            The target values (class labels in classification, real numbers in\n            regression).\n\n        max_samples : int or float, optional (default=None)\n            Argument to use instead of self.max_samples.\n\n        max_depth : int, optional (default=None)\n            Override value used when constructing base estimator. Only\n            supported if the base estimator has a max_depth parameter.\n\n        sample_weight : array-like of shape (n_samples,), default=None\n            Sample weights. If None, then samples are equally weighted.\n            Note that this is supported only if the base estimator supports\n            sample weighting.\n\n        Returns\n        -------\n        self : object\n        '
    random_state = check_random_state(self.random_state)
    (X, y) = check_X_y(X, y, ['csr', 'csc'], dtype=None, force_all_finite=False, multi_output=True)
    if (sample_weight is not None):
        sample_weight = check_array(sample_weight, ensure_2d=False)
        check_consistent_length(y, sample_weight)
    (n_samples, self.n_features_) = X.shape
    self._n_samples = n_samples
    y = self._validate_y(y)
    self._validate_estimator()
    if (max_depth is not None):
        self.base_estimator_.max_depth = max_depth
    if (max_samples is None):
        max_samples = self.max_samples
    elif (not isinstance(max_samples, numbers.Integral)):
        max_samples = int((max_samples * X.shape[0]))
    if (not (0 < max_samples <= X.shape[0])):
        raise ValueError('max_samples must be in (0, n_samples]')
    self._max_samples = max_samples
    if isinstance(self.max_features, numbers.Integral):
        max_features = self.max_features
    elif isinstance(self.max_features, np.float):
        max_features = (self.max_features * self.n_features_)
    else:
        raise ValueError('max_features must be int or float')
    if (not (0 < max_features <= self.n_features_)):
        raise ValueError('max_features must be in (0, n_features]')
    max_features = max(1, int(max_features))
    self._max_features = max_features
    if ((not self.bootstrap) and self.oob_score):
        raise ValueError('Out of bag estimation only available if bootstrap=True')
    if (self.warm_start and self.oob_score):
        raise ValueError('Out of bag estimate only available if warm_start=False')
    if (hasattr(self, 'oob_score_') and self.warm_start):
        del self.oob_score_
    if ((not self.warm_start) or (not hasattr(self, 'estimators_'))):
        self.estimators_ = []
        self.estimators_features_ = []
    n_more_estimators = (self.n_estimators - len(self.estimators_))
    if (n_more_estimators < 0):
        raise ValueError(('n_estimators=%d must be larger or equal to len(estimators_)=%d when warm_start==True' % (self.n_estimators, len(self.estimators_))))
    elif (n_more_estimators == 0):
        warn('Warm-start fitting without increasing n_estimators does not fit new trees.')
        return self
    (n_jobs, n_estimators, starts) = _partition_estimators(n_more_estimators, self.n_jobs)
    total_n_estimators = sum(n_estimators)
    if (self.warm_start and (len(self.estimators_) > 0)):
        random_state.randint(MAX_INT, size=len(self.estimators_))
    seeds = random_state.randint(MAX_INT, size=n_more_estimators)
    self._seeds = seeds
    all_results = Parallel(n_jobs=n_jobs, verbose=self.verbose, **self._parallel_args())((delayed(_parallel_build_estimators)(n_estimators[i], self, X, y, sample_weight, seeds[starts[i]:starts[(i + 1)]], total_n_estimators, verbose=self.verbose) for i in range(n_jobs)))
    self.estimators_ += list(itertools.chain.from_iterable((t[0] for t in all_results)))
    self.estimators_features_ += list(itertools.chain.from_iterable((t[1] for t in all_results)))
    if self.oob_score:
        self._set_oob_score(X, y)
    return self