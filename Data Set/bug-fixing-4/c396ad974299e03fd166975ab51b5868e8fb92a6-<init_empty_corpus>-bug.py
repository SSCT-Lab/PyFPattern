def init_empty_corpus(self):
    '\n        Initialize an empty corpus. If the corpora are to be treated as lists, simply\n        initialize an empty list. If serialization is used, initialize an empty corpus\n        of the class `gensim.corpora.MmCorpus`.\n\n        '
    if self.serialized:
        MmCorpus.serialize(self.serialization_path, [])
        self.corpus = MmCorpus(self.serialization_path)
    else:
        self.corpus = []