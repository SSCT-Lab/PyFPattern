def build_from_word2vec(self):
    'Build an Annoy index using word vectors from a Word2Vec model'
    self.model.init_sims()
    return self._build_from_model(self.model.wv.syn0norm, self.model.wv.index2word, self.model.vector_size)