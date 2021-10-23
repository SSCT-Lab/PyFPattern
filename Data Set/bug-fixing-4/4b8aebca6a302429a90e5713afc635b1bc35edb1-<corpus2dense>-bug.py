def corpus2dense(corpus, num_terms, num_docs=None, dtype=np.float32):
    '\n    Convert corpus into a dense np array (documents will be columns). You\n    must supply the number of features `num_terms`, because dimensionality\n    cannot be deduced from the sparse vectors alone.\n\n    You can optionally supply `num_docs` (=the corpus length) as well, so that\n    a more memory-efficient code path is taken.\n\n    This is the mirror function to `Dense2Corpus`.\n\n    '
    if (num_docs is not None):
        (docno, result) = ((- 1), np.empty((num_terms, num_docs), dtype=dtype))
        for (docno, doc) in enumerate(corpus):
            result[:, docno] = sparse2full(doc, num_terms)
        assert ((docno + 1) == num_docs)
    else:
        result = np.column_stack((sparse2full(doc, num_terms) for doc in corpus))
    return result.astype(dtype)