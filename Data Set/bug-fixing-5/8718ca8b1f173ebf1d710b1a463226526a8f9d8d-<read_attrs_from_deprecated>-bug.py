def read_attrs_from_deprecated(freqs_loc, clusters_loc):
    with msg.loading('Counting frequencies...'):
        (probs, oov_prob) = (read_freqs(freqs_loc) if (freqs_loc is not None) else ({
            
        }, (- 20)))
    msg.good('Counted frequencies')
    with msg.loading('Reading clusters...'):
        clusters = (read_clusters(clusters_loc) if clusters_loc else {
            
        })
    msg.good('Read clusters')
    lex_attrs = []
    sorted_probs = sorted(probs.items(), key=(lambda item: item[1]), reverse=True)
    for (i, (word, prob)) in tqdm(enumerate(sorted_probs)):
        attrs = {
            'orth': word,
            'id': i,
            'prob': prob,
        }
        if (word in clusters):
            attrs['cluster'] = int(clusters[word][::(- 1)], 2)
        else:
            attrs['cluster'] = 0
        lex_attrs.append(attrs)
    return lex_attrs