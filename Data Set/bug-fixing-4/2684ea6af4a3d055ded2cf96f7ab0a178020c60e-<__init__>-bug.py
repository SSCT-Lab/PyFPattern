def __init__(self, model=None, num_trees=None):
    self.index = None
    self.labels = None
    self.model = model
    self.num_trees = num_trees
    if (model and num_trees):
        if isinstance(self.model, Doc2Vec):
            self.build_from_doc2vec()
        elif isinstance(self.model, Word2Vec):
            self.build_from_word2vec()
        elif isinstance(self.model, KeyedVectors):
            self.build_from_keyedvectors()
        else:
            raise ValueError('Only a Word2Vec, Doc2Vec or KeyedVectors instance can be used')