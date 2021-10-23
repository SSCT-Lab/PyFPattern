def corpus2csc(corpus, num_terms=None, dtype=np.float64, num_docs=None, num_nnz=None, printprogress=0):
    'Convert a streamed corpus in BoW format into a sparse matrix `scipy.sparse.csc_matrix`,\n    with documents as columns.\n\n    Notes\n    -----\n    If the number of terms, documents and non-zero elements is known, you can pass\n    them here as parameters and a more memory efficient code path will be taken.\n\n    Parameters\n    ----------\n    corpus : iterable of iterable of (int, number)\n        Input corpus in BoW format\n    num_terms : int, optional\n        If provided, the `num_terms` attributes in the corpus will be ignored.\n    dtype : data-type, optional\n        Data type of output matrix.\n    num_docs : int, optional\n        If provided, the `num_docs` attributes in the corpus will be ignored.\n    num_nnz : int, optional\n        If provided, the `num_nnz` attributes in the corpus will be ignored.\n    printprogress : int, optional\n        Print progress for every `printprogress` number of documents,\n        If 0 - nothing will be printed.\n\n    Returns\n    -------\n    scipy.sparse.csc_matrix\n        Sparse matrix inferred based on `corpus`.\n\n    See Also\n    --------\n    :class:`~gensim.matutils.Sparse2Corpus`\n\n    '
    try:
        if (num_terms is None):
            num_terms = corpus.num_terms
        if (num_docs is None):
            num_docs = corpus.num_docs
        if (num_nnz is None):
            num_nnz = corpus.num_nnz
    except AttributeError:
        pass
    if printprogress:
        logger.info('creating sparse matrix from corpus')
    if ((num_terms is not None) and (num_docs is not None) and (num_nnz is not None)):
        (posnow, indptr) = (0, [0])
        indices = np.empty((num_nnz,), dtype=np.int32)
        data = np.empty((num_nnz,), dtype=dtype)
        for (docno, doc) in enumerate(corpus):
            if (printprogress and ((docno % printprogress) == 0)):
                logger.info('PROGRESS: at document #%i/%i', docno, num_docs)
            posnext = (posnow + len(doc))
            indices[posnow:posnext] = [feature_id for (feature_id, _) in doc]
            data[posnow:posnext] = [feature_weight for (_, feature_weight) in doc]
            indptr.append(posnext)
            posnow = posnext
        assert (posnow == num_nnz), 'mismatch between supplied and computed number of non-zeros'
        result = scipy.sparse.csc_matrix((data, indices, indptr), shape=(num_terms, num_docs), dtype=dtype)
    else:
        (num_nnz, data, indices, indptr) = (0, [], [], [0])
        for (docno, doc) in enumerate(corpus):
            if (printprogress and ((docno % printprogress) == 0)):
                logger.info('PROGRESS: at document #%i', docno)
            indices.extend([feature_id for (feature_id, _) in doc])
            data.extend([feature_weight for (_, feature_weight) in doc])
            num_nnz += len(doc)
            indptr.append(num_nnz)
        if (num_terms is None):
            num_terms = ((max(indices) + 1) if indices else 0)
        num_docs = (len(indptr) - 1)
        data = np.asarray(data, dtype=dtype)
        indices = np.asarray(indices)
        result = scipy.sparse.csc_matrix((data, indices, indptr), shape=(num_terms, num_docs), dtype=dtype)
    return result