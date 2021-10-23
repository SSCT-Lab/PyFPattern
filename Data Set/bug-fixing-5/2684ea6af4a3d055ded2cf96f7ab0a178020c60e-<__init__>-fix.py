def __init__(self, model=None, num_trees=None):
    '\n        Parameters\n        ----------\n        model : :class:`~gensim.models.word2vec.Word2Vec`, :class:`~gensim.models.doc2vec.Doc2Vec` or\n                :class:`~gensim.models.keyedvectors.KeyedVectors`, optional\n            Model, that will be used as source for index.\n        num_trees : int, optional\n            Number of trees for Annoy indexer.\n\n        Examples\n        --------\n        >>> from gensim.similarities.index import AnnoyIndexer\n        >>> from gensim.models import Word2Vec\n        >>>\n        >>> sentences = [[\'cute\', \'cat\', \'say\', \'meow\'], [\'cute\', \'dog\', \'say\', \'woof\']]\n        >>> model = Word2Vec(sentences, min_count=1, seed=1)\n        >>>\n        >>> indexer = AnnoyIndexer(model, 2)\n        >>> model.most_similar("cat", topn=2, indexer=indexer)\n        [(\'cat\', 1.0), (\'dog\', 0.32011348009109497)]\n\n        '
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