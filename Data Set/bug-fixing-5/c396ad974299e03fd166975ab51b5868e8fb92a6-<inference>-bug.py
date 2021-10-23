def inference(self, chunk, author2doc, doc2author, rhot, collect_sstats=False, chunk_doc_idx=None):
    "\n        Given a chunk of sparse document vectors, update gamma (parameters\n        controlling the topic weights) for each author corresponding to the\n        documents in the chunk.\n\n        The whole input chunk of document is assumed to fit in RAM; chunking of\n        a large corpus must be done earlier in the pipeline.\n\n        If `collect_sstats` is True, also collect sufficient statistics needed\n        to update the model's topic-word distributions, and return a 2-tuple\n        `(gamma_chunk, sstats)`. Otherwise, return `(gamma_chunk, None)`.\n        `gamma_cunk` is of shape `len(chunk_authors) x self.num_topics`, where\n        `chunk_authors` is the number of authors in the documents in the\n        current chunk.\n\n        Avoids computing the `phi` variational parameter directly using the\n        optimization presented in **Lee, Seung: Algorithms for non-negative matrix factorization, NIPS 2001**.\n\n        "
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