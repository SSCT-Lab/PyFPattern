def score_samples(self, X):
    'Compute the pseudo-likelihood of X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix} shape (n_samples, n_features)\n            Values of the visible layer. Must be all-boolean (not checked).\n\n        Returns\n        -------\n        pseudo_likelihood : array-like, shape (n_samples,)\n            Value of the pseudo-likelihood (proxy for likelihood).\n\n        Notes\n        -----\n        This method is not deterministic: it computes a quantity called the\n        free energy on X, then on a randomly corrupted version of X, and\n        returns the log of the logistic function of the difference.\n        '
    check_is_fitted(self, 'components_')
    v = check_array(X, accept_sparse='csr')
    rng = check_random_state(self.random_state)
    ind = (np.arange(v.shape[0]), rng.randint(0, v.shape[1], v.shape[0]))
    if issparse(v):
        data = (((- 2) * v[ind]) + 1)
        v_ = (v + sp.csr_matrix((data.A.ravel(), ind), shape=v.shape))
    else:
        v_ = v.copy()
        v_[ind] = (1 - v_[ind])
    fe = self._free_energy(v)
    fe_ = self._free_energy(v_)
    return (v.shape[1] * log_logistic((fe_ - fe)))