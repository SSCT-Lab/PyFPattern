def inference(self, chunk, author2doc, doc2author, rhot, collect_sstats=False, chunk_doc_idx=None):
    'Give a `chunk` of sparse document vectors, update gamma for each author corresponding to the `chuck`.\n\n        Warnings\n        --------\n        The whole input chunk of document is assumed to fit in RAM, chunking of a large corpus must be done earlier\n        in the pipeline.\n\n        Avoids computing the `phi` variational parameter directly using the\n        optimization presented in `Lee, Seung: "Algorithms for non-negative matrix factorization", NIPS 2001\n        <https://papers.nips.cc/paper/1861-algorithms-for-non-negative-matrix-factorization.pdf>`_.\n\n        Parameters\n        ----------\n        chunk : iterable of list of (int, float)\n            Corpus in BoW format.\n        author2doc : dict of (str, list of int), optional\n            A dictionary where keys are the names of authors and values are lists of document IDs that the author\n            contributes to.\n        doc2author : dict of (int, list of str), optional\n            A dictionary where the keys are document IDs and the values are lists of author names.\n        rhot : float\n            Value of rho for conducting inference on documents.\n        collect_sstats : boolean, optional\n            If True - collect sufficient statistics needed to update the model\'s topic-word distributions, and return\n            `(gamma_chunk, sstats)`. Otherwise, return `(gamma_chunk, None)`. `gamma_chunk` is of shape\n            `len(chunk_authors) x self.num_topics`,where `chunk_authors` is the number of authors in the documents in\n            the current chunk.\n        chunk_doc_idx : numpy.ndarray, optional\n            Assigns the value for document index.\n\n        Returns\n        -------\n        (numpy.ndarray, numpy.ndarray)\n            gamma_chunk and sstats (if `collect_sstats == True`, otherwise - None)\n\n        '
    try:
        len(chunk)
    except TypeError:
        chunk = list(chunk)
    if (len(chunk) > 1):
        logger.debug('performing inference on a chunk of %i documents', len(chunk))
    if collect_sstats:
        sstats = np.zeros_like(self.expElogbeta)
    else:
        sstats = None
    converged = 0
    gamma_chunk = np.zeros((0, self.num_topics))
    for (d, doc) in enumerate(chunk):
        if (chunk_doc_idx is not None):
            doc_no = chunk_doc_idx[d]
        else:
            doc_no = d
        if (doc and (not isinstance(doc[0][0], (six.integer_types + (np.integer,))))):
            ids = [int(idx) for (idx, _) in doc]
        else:
            ids = [idx for (idx, _) in doc]
        cts = np.array([cnt for (_, cnt) in doc])
        authors_d = [self.author2id[a] for a in self.doc2author[doc_no]]
        gammad = self.state.gamma[authors_d, :]
        tilde_gamma = gammad.copy()
        Elogthetad = dirichlet_expectation(tilde_gamma)
        expElogthetad = np.exp(Elogthetad)
        expElogbetad = self.expElogbeta[:, ids]
        phinorm = self.compute_phinorm(expElogthetad, expElogbetad)
        for _ in xrange(self.iterations):
            lastgamma = tilde_gamma.copy()
            for (ai, a) in enumerate(authors_d):
                tilde_gamma[ai, :] = (self.alpha + ((len(self.author2doc[self.id2author[a]]) * expElogthetad[ai, :]) * np.dot((cts / phinorm), expElogbetad.T)))
            tilde_gamma = (((1 - rhot) * gammad) + (rhot * tilde_gamma))
            Elogthetad = dirichlet_expectation(tilde_gamma)
            expElogthetad = np.exp(Elogthetad)
            phinorm = self.compute_phinorm(expElogthetad, expElogbetad)
            meanchange_gamma = np.mean(abs((tilde_gamma - lastgamma)))
            gamma_condition = (meanchange_gamma < self.gamma_threshold)
            if gamma_condition:
                converged += 1
                break
        self.state.gamma[authors_d, :] = tilde_gamma
        gamma_chunk = np.vstack([gamma_chunk, tilde_gamma])
        if collect_sstats:
            expElogtheta_sum_a = expElogthetad.sum(axis=0)
            sstats[:, ids] += np.outer(expElogtheta_sum_a.T, (cts / phinorm))
    if (len(chunk) > 1):
        logger.debug('%i/%i documents converged within %i iterations', converged, len(chunk), self.iterations)
    if collect_sstats:
        sstats *= self.expElogbeta
    return (gamma_chunk, sstats)