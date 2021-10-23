def bound(self, chunk, chunk_doc_idx=None, subsample_ratio=1.0, author2doc=None, doc2author=None):
    '\n        Estimate the variational bound of documents from `corpus`:\n        E_q[log p(corpus)] - E_q[log q(corpus)]\n\n        There are basically two use cases of this method:\n        1. `chunk` is a subset of the training corpus, and `chunk_doc_idx` is provided,\n        indicating the indexes of the documents in the training corpus.\n        2. `chunk` is a test set (held-out data), and author2doc and doc2author\n        corrsponding to this test set are provided. There must not be any new authors\n        passed to this method. `chunk_doc_idx` is not needed in this case.\n\n        To obtain the per-word bound, compute:\n\n        >>> corpus_words = sum(cnt for document in corpus for _, cnt in document)\n        >>> model.bound(corpus, author2doc=author2doc, doc2author=doc2author) / corpus_words\n\n        '
    _lambda = self.state.get_lambda()
    Elogbeta = dirichlet_expectation(_lambda)
    expElogbeta = np.exp(Elogbeta)
    gamma = self.state.gamma
    if ((author2doc is None) and (doc2author is None)):
        author2doc = self.author2doc
        doc2author = self.doc2author
        if (not chunk_doc_idx):
            raise ValueError('Either author dictionaries or chunk_doc_idx must be provided. Consult documentation of bound method.')
    elif ((author2doc is not None) and (doc2author is not None)):
        for a in author2doc.keys():
            if (not self.author2doc.get(a)):
                raise ValueError('bound cannot be called with authors not seen during training.')
        if chunk_doc_idx:
            raise ValueError('Either author dictionaries or chunk_doc_idx must be provided, not both. Consult documentation of bound method.')
    else:
        raise ValueError('Either both author2doc and doc2author should be provided, or neither. Consult documentation of bound method.')
    Elogtheta = dirichlet_expectation(gamma)
    expElogtheta = np.exp(Elogtheta)
    word_score = 0.0
    theta_score = 0.0
    for (d, doc) in enumerate(chunk):
        if chunk_doc_idx:
            doc_no = chunk_doc_idx[d]
        else:
            doc_no = d
        authors_d = [self.author2id[a] for a in self.doc2author[doc_no]]
        ids = np.array([id for (id, _) in doc])
        cts = np.array([cnt for (_, cnt) in doc])
        if ((d % self.chunksize) == 0):
            logger.debug('bound: at document #%i in chunk', d)
        phinorm = self.compute_phinorm(expElogtheta[authors_d, :], expElogbeta[:, ids])
        word_score += ((np.log((1.0 / len(authors_d))) * sum(cts)) + cts.dot(np.log(phinorm)))
    word_score *= subsample_ratio
    for a in author2doc.keys():
        a = self.author2id[a]
        theta_score += np.sum(((self.alpha - gamma[a, :]) * Elogtheta[a, :]))
        theta_score += np.sum((gammaln(gamma[a, :]) - gammaln(self.alpha)))
        theta_score += (gammaln(np.sum(self.alpha)) - gammaln(np.sum(gamma[a, :])))
    theta_score *= (self.num_authors / len(author2doc))
    beta_score = 0.0
    beta_score += np.sum(((self.eta - _lambda) * Elogbeta))
    beta_score += np.sum((gammaln(_lambda) - gammaln(self.eta)))
    sum_eta = np.sum(self.eta)
    beta_score += np.sum((gammaln(sum_eta) - gammaln(np.sum(_lambda, 1))))
    total_score = ((word_score + theta_score) + beta_score)
    return total_score