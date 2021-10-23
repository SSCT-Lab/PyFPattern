def _add_word_to_result(result, counts, word, weights, vocab_size):
    word_id = len(result.vocab)
    if (word in result.vocab):
        logger.warning("duplicate word '%s' in word2vec file, ignoring all but first", word)
        return
    if (counts is None):
        word_count = (vocab_size - word_id)
    elif (word in counts):
        word_count = counts[word]
    else:
        logger.warning("vocabulary file is incomplete: '%s' is missing", word)
        word_count = None
    result.vocab[word] = gensim.models.keyedvectors.Vocab(index=word_id, count=word_count)
    result.vectors[word_id] = weights
    result.index2word.append(word)