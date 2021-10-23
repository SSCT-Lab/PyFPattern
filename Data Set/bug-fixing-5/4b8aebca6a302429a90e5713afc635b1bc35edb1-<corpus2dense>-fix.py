def corpus2dense(corpus, num_terms, num_docs=None, dtype=np.float32):
    'Convert corpus into a dense numpy array (documents will be columns).\n\n    Parameters\n    ----------\n    corpus : iterable of iterable of (int, number)\n        Input corpus in BoW format.\n    num_terms : int\n        Number of terms in dictionary (will be used as size of output vector.\n    num_docs : int, optional\n        Number of documents in corpus.\n    dtype : data-type, optional\n        Data type of output matrix\n\n    Returns\n    -------\n    numpy.ndarray\n        Dense array that present `corpus`.\n\n    See Also\n    --------\n    :class:`~gensim.matutils.Dense2Corpus`\n\n    '
    if (num_docs is not None):
        (docno, result) = ((- 1), np.empty((num_terms, num_docs), dtype=dtype))
        for (docno, doc) in enumerate(corpus):
            result[:, docno] = sparse2full(doc, num_terms)
        assert ((docno + 1) == num_docs)
    else:
        result = np.column_stack((sparse2full(doc, num_terms) for doc in corpus))
    return result.astype(dtype)