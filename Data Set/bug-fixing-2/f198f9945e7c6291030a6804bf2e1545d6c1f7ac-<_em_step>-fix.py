

def _em_step(self, X, total_samples, batch_update, parallel=None):
    'EM update for 1 iteration.\n\n        update `_component` by batch VB or online VB.\n\n        Parameters\n        ----------\n        X : array-like or sparse matrix, shape=(n_samples, n_features)\n            Document word matrix.\n\n        total_samples : integer\n            Total number of documents. It is only used when\n            batch_update is `False`.\n\n        batch_update : boolean\n            Parameter that controls updating method.\n            `True` for batch learning, `False` for online learning.\n\n        parallel : joblib.Parallel\n            Pre-initialized instance of joblib.Parallel\n\n        Returns\n        -------\n        doc_topic_distr : array, shape=(n_samples, n_components)\n            Unnormalized document topic distribution.\n        '
    (_, suff_stats) = self._e_step(X, cal_sstats=True, random_init=True, parallel=parallel)
    if batch_update:
        self.components_ = (self.topic_word_prior_ + suff_stats)
    else:
        weight = np.power((self.learning_offset + self.n_batch_iter_), (- self.learning_decay))
        doc_ratio = (float(total_samples) / X.shape[0])
        self.components_ *= (1 - weight)
        self.components_ += (weight * (self.topic_word_prior_ + (doc_ratio * suff_stats)))
    self.exp_dirichlet_component_ = np.exp(_dirichlet_expectation_2d(self.components_))
    self.n_batch_iter_ += 1
    return
