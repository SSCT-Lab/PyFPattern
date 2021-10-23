def load(self, fname):
    "Load AnnoyIndexer instance\n\n        Parameters\n        ----------\n        fname : str\n            Path to dump with AnnoyIndexer.\n\n        Examples\n        --------\n        >>> from gensim.similarities.index import AnnoyIndexer\n        >>> from gensim.models import Word2Vec\n        >>> from tempfile import mkstemp\n        >>>\n        >>> sentences = [['cute', 'cat', 'say', 'meow'], ['cute', 'dog', 'say', 'woof']]\n        >>> model = Word2Vec(sentences, min_count=1, seed=1, iter=10)\n        >>>\n        >>> indexer = AnnoyIndexer(model, 2)\n        >>> _, temp_fn = mkstemp()\n        >>> indexer.save(temp_fn)\n        >>>\n        >>> new_indexer = AnnoyIndexer()\n        >>> new_indexer.load(temp_fn)\n        >>> new_indexer.model = model\n\n        "
    fname_dict = (fname + '.d')
    if (not (os.path.exists(fname) and os.path.exists(fname_dict))):
        raise IOError(("Can't find index files '%s' and '%s' - Unable to restore AnnoyIndexer state." % (fname, fname_dict)))
    else:
        with smart_open(fname_dict) as f:
            d = _pickle.loads(f.read())
        self.num_trees = d['num_trees']
        self.index = AnnoyIndex(d['f'])
        self.index.load(fname)
        self.labels = d['labels']