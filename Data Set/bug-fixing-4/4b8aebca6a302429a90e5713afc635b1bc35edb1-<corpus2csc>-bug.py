def corpus2csc(corpus, num_terms=None, dtype=np.float64, num_docs=None, num_nnz=None, printprogress=0):
    '\n    Convert a streamed corpus into a sparse matrix, in scipy.sparse.csc_matrix format,\n    with documents as columns.\n\n    If the number of terms, documents and non-zero elements is known, you can pass\n    them here as parameters and a more memory efficient code path will be taken.\n\n    The input corpus may be a non-repeatable stream (generator).\n\n    This is the mirror function to `Sparse2Corpus`.\n\n    '
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