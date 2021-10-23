def sparse2full(doc, length):
    'Convert a document in BoW format into dense numpy array.\n\n    Parameters\n    ----------\n    doc : list of (int, number)\n        Document in BoW format\n    length : int\n        Length of result vector\n\n    Returns\n    -------\n    numpy.ndarray\n        Dense variant of `doc` vector.\n\n    See Also\n    --------\n    :func:`~gensim.matutils.full2sparse`\n\n    '
    result = np.zeros(length, dtype=np.float32)
    doc = ((int(id_), float(val_)) for (id_, val_) in doc)
    doc = dict(doc)
    result[list(doc)] = list(itervalues(doc))
    return result