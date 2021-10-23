def build_from_keyedvectors(self):
    'Build an Annoy index using word vectors from a KeyedVectors model.'
    self.model.init_sims()
    return self._build_from_model(self.model.syn0norm, self.model.index2word, self.model.vector_size)