def extend_corpus(self, corpus):
    '\n        Add new documents in `corpus` to `self.corpus`. If serialization is used,\n        then the entire corpus (`self.corpus`) is re-serialized and the new documents\n        are added in the process. If serialization is not used, the corpus, as a list\n        of documents, is simply extended.\n\n        '
    if self.serialized:
        if isinstance(corpus, MmCorpus):
            assert (self.corpus.input != corpus.input), 'Input corpus cannot have the same file path as the model corpus (serialization_path).'
        corpus_chain = chain(self.corpus, corpus)
        copyfile(self.serialization_path, (self.serialization_path + '.tmp'))
        self.corpus.input = (self.serialization_path + '.tmp')
        MmCorpus.serialize(self.serialization_path, corpus_chain)
        self.corpus = MmCorpus(self.serialization_path)
        remove((self.serialization_path + '.tmp'))
    else:
        assert isinstance(corpus, list), 'If serialized == False, all input corpora must be lists.'
        self.corpus.extend(corpus)