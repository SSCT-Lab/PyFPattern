def init_empty_corpus(self):
    'Initialize an empty corpus.\n        If the corpora are to be treated as lists, simply initialize an empty list.\n        If serialization is used, initialize an empty corpus using :class:`~gensim.corpora.mmcorpus.MmCorpus`.\n\n        '
    if self.serialized:
        MmCorpus.serialize(self.serialization_path, [])
        self.corpus = MmCorpus(self.serialization_path)
    else:
        self.corpus = []