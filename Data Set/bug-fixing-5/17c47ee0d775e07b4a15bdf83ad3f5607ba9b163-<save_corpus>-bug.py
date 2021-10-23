@staticmethod
def save_corpus(fname, corpus, id2word=None, progress_cnt=10000, metadata=False):
    "\n        Save a corpus in the UCI Bag-of-Words format.\n\n        There are actually two files saved: `fname` and `fname.vocab`, where\n        `fname.vocab` is the vocabulary file.\n\n        This function is automatically called by `UciCorpus.serialize`; don't\n        call it directly, call `serialize` instead.\n        "
    if (id2word is None):
        logger.info('no word id mapping provided; initializing from corpus')
        id2word = utils.dict_from_corpus(corpus)
        num_terms = len(id2word)
    else:
        num_terms = (1 + max(([(- 1)] + id2word.keys())))
    fname_vocab = utils.smart_extension(fname, '.vocab')
    logger.info('saving vocabulary of %i words to %s', num_terms, fname_vocab)
    with utils.smart_open(fname_vocab, 'wb') as fout:
        for featureid in xrange(num_terms):
            fout.write(utils.to_utf8(('%s\n' % id2word.get(featureid, '---'))))
    logger.info('storing corpus in UCI Bag-of-Words format: %s', fname)
    return UciWriter.write_corpus(fname, corpus, index=True, progress_cnt=progress_cnt)