def build_from_doc2vec(self):
    'Build an Annoy index using document vectors from a Doc2Vec model'
    docvecs = self.model.docvecs
    docvecs.init_sims()
    labels = [docvecs.index_to_doctag(i) for i in range(0, docvecs.count)]
    return self._build_from_model(docvecs.doctag_syn0norm, labels, self.model.vector_size)