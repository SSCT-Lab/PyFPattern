def get_new_author_topics(self, corpus, minimum_probability=None):
    'Infers topics for new author.\n\n        Infers a topic distribution for a new author over the passed corpus of docs,\n        assuming that all documents are from this single new author.\n\n        Parameters\n        ----------\n        corpus : iterable of iterable of (int, int)\n            Corpus in BoW format.\n        minimum_probability : float, optional\n            Ignore topics with probability below this value, if None - 1e-8 is used.\n\n        Returns\n        -------\n        list of (int, float)\n            Topic distribution for the given `corpus`.\n\n        '

    def rho():
        return pow(((self.offset + 1) + 1), (- self.decay))

    def rollback_new_author_chages():
        self.state.gamma = self.state.gamma[0:(- 1)]
        del self.author2doc[new_author_name]
        a_id = self.author2id[new_author_name]
        del self.id2author[a_id]
        del self.author2id[new_author_name]
        for new_doc_id in corpus_doc_idx:
            del self.doc2author[new_doc_id]
    try:
        len_input_corpus = len(corpus)
    except TypeError:
        logger.warning('input corpus stream has no len(); counting documents')
        len_input_corpus = sum((1 for _ in corpus))
    if (len_input_corpus == 0):
        raise ValueError('AuthorTopicModel.get_new_author_topics() called with an empty corpus')
    new_author_name = 'placeholder_name'
    corpus_doc_idx = list(range(self.total_docs, (self.total_docs + len_input_corpus)))
    num_new_authors = 1
    author_id = self.num_authors
    if (new_author_name in self.author2id):
        raise ValueError("self.author2id already has 'placeholder_name' author")
    self.author2id[new_author_name] = author_id
    self.id2author[author_id] = new_author_name
    self.author2doc[new_author_name] = corpus_doc_idx
    for new_doc_id in corpus_doc_idx:
        self.doc2author[new_doc_id] = [new_author_name]
    gamma_new = self.random_state.gamma(100.0, (1.0 / 100.0), (num_new_authors, self.num_topics))
    self.state.gamma = np.vstack([self.state.gamma, gamma_new])
    try:
        (gammat, _) = self.inference(corpus, self.author2doc, self.doc2author, rho(), collect_sstats=False, chunk_doc_idx=corpus_doc_idx)
        new_author_topics = self.get_author_topics(new_author_name, minimum_probability)
    finally:
        rollback_new_author_chages()
    return new_author_topics