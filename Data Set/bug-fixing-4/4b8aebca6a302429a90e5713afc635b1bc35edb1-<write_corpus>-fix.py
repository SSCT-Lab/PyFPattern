@staticmethod
def write_corpus(fname, corpus, progress_cnt=1000, index=False, num_terms=None, metadata=False):
    'Save the corpus to disk in Matrix Market format.\n\n        Parameters\n        ----------\n        fname : str\n            Filename of the resulting file.\n        corpus : iterable of iterable of (int, float)\n            Corpus in Bow format\n        progress_cnt : int, optional\n            Print progress for every `progress_cnt` number of documents.\n        index : bool, optional\n            If True, the offsets will be return, otherwise return None.\n        num_terms : int, optional\n            If provided, the `num_terms` attributes in the corpus will be ignored.\n        metadata : bool, optional\n            If True, a metadata file will be generated.\n\n        Returns\n        -------\n        offsets : {list of int, None}\n            List of offsets or nothing.\n\n        Notes\n        -----\n        Documents are processed one at a time, so the whole corpus is allowed to be larger than the available RAM.\n\n        See Also\n        --------\n        :func:`~gensim.corpora.mmcorpus.MmCorpus.save_corpus`\n\n        '
    mw = MmWriter(fname)
    mw.write_headers((- 1), (- 1), (- 1))
    (_num_terms, num_nnz) = (0, 0)
    (docno, poslast) = ((- 1), (- 1))
    offsets = []
    if hasattr(corpus, 'metadata'):
        orig_metadata = corpus.metadata
        corpus.metadata = metadata
        if metadata:
            docno2metadata = {
                
            }
    else:
        metadata = False
    for (docno, doc) in enumerate(corpus):
        if metadata:
            (bow, data) = doc
            docno2metadata[docno] = data
        else:
            bow = doc
        if ((docno % progress_cnt) == 0):
            logger.info('PROGRESS: saving document #%i', docno)
        if index:
            posnow = mw.fout.tell()
            if (posnow == poslast):
                offsets[(- 1)] = (- 1)
            offsets.append(posnow)
            poslast = posnow
        (max_id, veclen) = mw.write_vector(docno, bow)
        _num_terms = max(_num_terms, (1 + max_id))
        num_nnz += veclen
    if metadata:
        utils.pickle(docno2metadata, (fname + '.metadata.cpickle'))
        corpus.metadata = orig_metadata
    num_docs = (docno + 1)
    num_terms = (num_terms or _num_terms)
    if ((num_docs * num_terms) != 0):
        logger.info('saved %ix%i matrix, density=%.3f%% (%i/%i)', num_docs, num_terms, ((100.0 * num_nnz) / (num_docs * num_terms)), num_nnz, (num_docs * num_terms))
    mw.fake_headers(num_docs, num_terms, num_nnz)
    mw.close()
    if index:
        return offsets