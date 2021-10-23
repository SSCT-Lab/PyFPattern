def encode_sentences(sentences, vocab=None, invalid_label=(- 1), invalid_key='\n', start_label=0):
    "Encode sentences and (optionally) build a mapping\n    from string tokens to integer indices. Unknown keys\n    will be added to vocabulary.\n\n    Parameters\n    ----------\n    sentences : list of list of str\n        A list of sentences to encode. Each sentence\n        should be a list of string tokens.\n    vocab : None or dict of str -> int\n        Optional input Vocabulary\n    invalid_label : int, default -1\n        Index for invalid token, like <end-of-sentence>\n    invalid_key : str, default '\n'\n        Key for invalid token. Use '\n' for end\n        of sentence by default.\n    start_label : int\n        lowest index.\n\n    Returns\n    -------\n    result : list of list of int\n        encoded sentences\n    vocab : dict of str -> int\n        result vocabulary\n    "
    idx = start_label
    if (vocab is None):
        vocab = {
            invalid_key: invalid_label,
        }
        new_vocab = True
    else:
        new_vocab = False
    res = []
    for sent in sentences:
        coded = []
        for word in sent:
            if (word not in vocab):
                assert new_vocab, ('Unknown token %s' % word)
                if (idx == invalid_label):
                    idx += 1
                vocab[word] = idx
                idx += 1
            coded.append(vocab[word])
        res.append(coded)
    return (res, vocab)