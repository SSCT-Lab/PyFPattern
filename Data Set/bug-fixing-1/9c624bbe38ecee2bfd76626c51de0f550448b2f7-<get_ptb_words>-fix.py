

def get_ptb_words():
    "Gets the Penn Tree Bank dataset as long word sequences.\n\n    `Penn Tree Bank <https://web.archive.org/web/19970614160127/http://www.cis.upenn.edu/~treebank/>`_\n    is originally a corpus of English sentences with linguistic structure\n    annotations. This function uses a variant distributed at\n    `https://github.com/wojzaremba/lstm <https://github.com/wojzaremba/lstm>`_,\n    which omits the annotation and splits the dataset into three parts:\n    training, validation, and test.\n\n    This function returns the training, validation, and test sets, each of\n    which is represented as a long array of word IDs. All sentences in the\n    dataset are concatenated by End-of-Sentence mark '<eos>', which is treated\n    as one of the vocabulary.\n\n    Returns:\n        tuple of numpy.ndarray: Int32 vectors of word IDs.\n\n    .. Seealso::\n       Use :func:`get_ptb_words_vocabulary` to get the mapping between the\n       words and word IDs.\n\n    "
    train = _retrieve_ptb_words('train.npz', _train_url)
    valid = _retrieve_ptb_words('valid.npz', _valid_url)
    test = _retrieve_ptb_words('test.npz', _test_url)
    return (train, valid, test)
