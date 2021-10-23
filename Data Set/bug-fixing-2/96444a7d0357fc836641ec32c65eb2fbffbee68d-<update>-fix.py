

def update(self, corpus=None, author2doc=None, doc2author=None, chunksize=None, decay=None, offset=None, passes=None, update_every=None, eval_every=None, iterations=None, gamma_threshold=None, chunks_as_numpy=False):
    "Train the model with new documents, by EM-iterating over `corpus` until the topics converge (or until the\n        maximum number of allowed iterations is reached).\n\n        Notes\n        -----\n        This update also supports updating an already trained model (self)\n        with new documents from `corpus`: the two models are then merged in proportion to the number of old vs. new\n        documents. This feature is still experimental for non-stationary input streams.\n\n        For stationary input (no topic drift in new documents), on the other hand, this equals the online update of\n        `Hoffman et al. Stochastic Variational Inference\n        <http://www.jmlr.org/papers/volume14/hoffman13a/hoffman13a.pdf>`_ and is guaranteed to converge for any `decay`\n        in (0.5, 1.0>. Additionally, for smaller `corpus` sizes, an increasing `offset` may be beneficial (see\n        Table 1 in Hoffman et al.)\n\n        If update is called with authors that already exist in the model, it will resume training on not only new\n        documents for that author, but also the previously seen documents. This is necessary for those authors' topic\n        distributions to converge.\n\n        Every time `update(corpus, author2doc)` is called, the new documents are to appended to all the previously seen\n        documents, and author2doc is combined with the previously seen authors.\n\n        To resume training on all the data seen by the model, simply call\n        :meth:`~gensim.models.atmodel.AuthorTopicModel.update`.\n\n        It is not possible to add new authors to existing documents, as all documents in `corpus` are assumed to be\n        new documents.\n\n        Parameters\n        ----------\n        corpus : iterable of list of (int, float)\n            The corpus in BoW format.\n        author2doc : dict of (str, list of int), optional\n            A dictionary where keys are the names of authors and values are lists of document IDs that the author\n            contributes to.\n        doc2author : dict of (int, list of str), optional\n            A dictionary where the keys are document IDs and the values are lists of author names.\n        chunksize : int, optional\n            Controls the size of the mini-batches.\n        decay : float, optional\n            Controls how old documents are forgotten.\n        offset : float, optional\n            Controls down-weighting of iterations.\n        passes : int, optional\n            Number of times the model makes a pass over the entire training data.\n        update_every : int, optional\n            Make updates in topic probability for latest mini-batch.\n        eval_every : int, optional\n            Calculate and estimate log perplexity for latest mini-batch.\n        iterations : int, optional\n            Maximum number of times the model loops over each document\n        gamma_threshold : float, optional\n            Threshold value of gamma(topic difference between consecutive two topics)\n            until which the iterations continue.\n        chunks_as_numpy : bool, optional\n            Whether each chunk passed to :meth:`~gensim.models.atmodel.AuthorTopicModel.inference` should be a numpy\n            array of not. Numpy can in some settings turn the term IDs into floats, these will be converted back into\n            integers in inference, which incurs a performance hit. For distributed computing (not supported now)\n            it may be desirable to keep the chunks as numpy arrays.\n\n        "
    if (decay is None):
        decay = self.decay
    if (offset is None):
        offset = self.offset
    if (passes is None):
        passes = self.passes
    if (update_every is None):
        update_every = self.update_every
    if (eval_every is None):
        eval_every = self.eval_every
    if (iterations is None):
        iterations = self.iterations
    if (gamma_threshold is None):
        gamma_threshold = self.gamma_threshold
    author2doc = deepcopy(author2doc)
    doc2author = deepcopy(doc2author)
    if (corpus is None):
        assert (self.total_docs > 0), 'update() was called with no documents to train on.'
        train_corpus_idx = [d for d in xrange(self.total_docs)]
        num_input_authors = len(self.author2doc)
    else:
        if ((doc2author is None) and (author2doc is None)):
            raise ValueError('at least one of author2doc/doc2author must be specified, to establish input space dimensionality')
        if (doc2author is None):
            doc2author = construct_doc2author(corpus, author2doc)
        elif (author2doc is None):
            author2doc = construct_author2doc(doc2author)
        num_input_authors = len(author2doc)
        try:
            len_input_corpus = len(corpus)
        except TypeError:
            logger.warning('input corpus stream has no len(); counting documents')
            len_input_corpus = sum((1 for _ in corpus))
        if (len_input_corpus == 0):
            logger.warning('AuthorTopicModel.update() called with an empty corpus')
            return
        self.total_docs += len_input_corpus
        self.extend_corpus(corpus)
        new_authors = []
        for a in sorted(author2doc.keys()):
            if (not self.author2doc.get(a)):
                new_authors.append(a)
        num_new_authors = len(new_authors)
        for (a_id, a_name) in enumerate(new_authors):
            self.author2id[a_name] = (a_id + self.num_authors)
            self.id2author[(a_id + self.num_authors)] = a_name
        self.num_authors += num_new_authors
        gamma_new = self.random_state.gamma(100.0, (1.0 / 100.0), (num_new_authors, self.num_topics))
        self.state.gamma = np.vstack([self.state.gamma, gamma_new])
        for (a, doc_ids) in author2doc.items():
            doc_ids = [((d + self.total_docs) - len_input_corpus) for d in doc_ids]
        for (a, doc_ids) in author2doc.items():
            if self.author2doc.get(a):
                self.author2doc[a].extend(doc_ids)
            else:
                self.author2doc[a] = doc_ids
        for (d, a_list) in doc2author.items():
            self.doc2author[d] = a_list
        train_corpus_idx = set()
        for doc_ids in self.author2doc.values():
            train_corpus_idx.update(doc_ids)
        train_corpus_idx = sorted(train_corpus_idx)
    lencorpus = len(train_corpus_idx)
    if (chunksize is None):
        chunksize = min(lencorpus, self.chunksize)
    self.state.numdocs += lencorpus
    if update_every:
        updatetype = 'online'
        updateafter = min(lencorpus, ((update_every * self.numworkers) * chunksize))
    else:
        updatetype = 'batch'
        updateafter = lencorpus
    evalafter = min(lencorpus, (((eval_every or 0) * self.numworkers) * chunksize))
    updates_per_pass = max(1, (lencorpus / updateafter))
    logger.info('running %s author-topic training, %s topics, %s authors, %i passes over the supplied corpus of %i documents, updating model once every %i documents, evaluating perplexity every %i documents, iterating %ix with a convergence threshold of %f', updatetype, self.num_topics, num_input_authors, passes, lencorpus, updateafter, evalafter, iterations, gamma_threshold)
    if ((updates_per_pass * passes) < 10):
        logger.warning('too few updates, training might not converge; consider increasing the number of passes or iterations to improve accuracy')

    def rho():
        return pow(((offset + pass_) + (self.num_updates / chunksize)), (- decay))
    for pass_ in xrange(passes):
        if self.dispatcher:
            logger.info('initializing %s workers', self.numworkers)
            self.dispatcher.reset(self.state)
        else:
            other = AuthorTopicState(self.eta, self.state.sstats.shape, (0, 0))
        dirty = False
        reallen = 0
        for (chunk_no, chunk_doc_idx) in enumerate(utils.grouper(train_corpus_idx, chunksize, as_numpy=chunks_as_numpy)):
            chunk = [self.corpus[d] for d in chunk_doc_idx]
            reallen += len(chunk)
            if (eval_every and ((reallen == lencorpus) or (((chunk_no + 1) % (eval_every * self.numworkers)) == 0))):
                self.log_perplexity(chunk, chunk_doc_idx, total_docs=lencorpus)
            if self.dispatcher:
                logger.info('PROGRESS: pass %i, dispatching documents up to #%i/%i', pass_, ((chunk_no * chunksize) + len(chunk)), lencorpus)
                self.dispatcher.putjob(chunk)
            else:
                logger.info('PROGRESS: pass %i, at document #%i/%i', pass_, ((chunk_no * chunksize) + len(chunk)), lencorpus)
                gammat = self.do_estep(chunk, self.author2doc, self.doc2author, rho(), other, chunk_doc_idx)
                if self.optimize_alpha:
                    self.update_alpha(gammat, rho())
            dirty = True
            del chunk
            if (update_every and (((chunk_no + 1) % (update_every * self.numworkers)) == 0)):
                if self.dispatcher:
                    logger.info('reached the end of input; now waiting for all remaining jobs to finish')
                    other = self.dispatcher.getstate()
                self.do_mstep(rho(), other, (pass_ > 0))
                del other
                if self.dispatcher:
                    logger.info('initializing workers')
                    self.dispatcher.reset(self.state)
                else:
                    other = AuthorTopicState(self.eta, self.state.sstats.shape, (0, 0))
                dirty = False
        if (reallen != lencorpus):
            raise RuntimeError("input corpus size changed during training (don't use generators as input)")
        if dirty:
            if self.dispatcher:
                logger.info('reached the end of input; now waiting for all remaining jobs to finish')
                other = self.dispatcher.getstate()
            self.do_mstep(rho(), other, (pass_ > 0))
            del other
