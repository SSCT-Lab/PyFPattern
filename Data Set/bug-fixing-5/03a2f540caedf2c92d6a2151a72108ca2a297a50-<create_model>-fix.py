def create_model(lang, probs, oov_prob, clusters, vectors_data, vector_keys, prune_vectors):
    print('Creating model...')
    lang_class = get_lang_class(lang)
    nlp = lang_class()
    for lexeme in nlp.vocab:
        lexeme.rank = 0
    lex_added = 0
    for (i, (word, prob)) in enumerate(tqdm(sorted(probs.items(), key=(lambda item: item[1]), reverse=True))):
        lexeme = nlp.vocab[word]
        lexeme.rank = i
        lexeme.prob = prob
        lexeme.is_oov = False
        if (word in clusters):
            lexeme.cluster = int(clusters[word][::(- 1)], 2)
        else:
            lexeme.cluster = 0
        lex_added += 1
    nlp.vocab.cfg.update({
        'oov_prob': oov_prob,
    })
    if vectors_data:
        nlp.vocab.vectors = Vectors(data=vectors_data, keys=vector_keys)
    if (prune_vectors >= 1):
        nlp.vocab.prune_vectors(prune_vectors)
    vec_added = len(nlp.vocab.vectors)
    prints('{} entries, {} vectors'.format(lex_added, vec_added), title='Sucessfully compiled vocab')
    return nlp