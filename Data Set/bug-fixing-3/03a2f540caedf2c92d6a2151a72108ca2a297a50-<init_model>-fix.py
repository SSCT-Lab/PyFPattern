@plac.annotations(lang=('model language', 'positional', None, str), output_dir=('model output directory', 'positional', None, Path), freqs_loc=('location of words frequencies file', 'positional', None, Path), clusters_loc=('optional: location of brown clusters data', 'option', 'c', str), vectors_loc=('optional: location of vectors file in GenSim text format', 'option', 'v', str), prune_vectors=('optional: number of vectors to prune to', 'option', 'V', int))
def init_model(_cmd, lang, output_dir, freqs_loc, clusters_loc=None, vectors_loc=None, prune_vectors=(- 1)):
    '\n    Create a new model from raw data, like word frequencies, Brown clusters\n    and word vectors.\n    '
    if (not freqs_loc.exists()):
        prints(freqs_loc, title="Can't find words frequencies file", exits=1)
    clusters_loc = ensure_path(clusters_loc)
    vectors_loc = ensure_path(vectors_loc)
    (probs, oov_prob) = read_freqs(freqs_loc)
    (vectors_data, vector_keys) = ((read_vectors(vectors_loc) if vectors_loc else None), None)
    clusters = (read_clusters(clusters_loc) if clusters_loc else {
        
    })
    nlp = create_model(lang, probs, oov_prob, clusters, vectors_data, vector_keys, prune_vectors)
    if (not output_dir.exists()):
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    return nlp