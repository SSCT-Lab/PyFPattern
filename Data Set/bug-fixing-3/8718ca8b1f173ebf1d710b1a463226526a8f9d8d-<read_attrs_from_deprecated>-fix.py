def read_attrs_from_deprecated(freqs_loc, clusters_loc):
    if (freqs_loc is not None):
        with msg.loading('Counting frequencies...'):
            (probs, _) = read_freqs(freqs_loc)
        msg.good('Counted frequencies')
    else:
        (probs, _) = ({
            
        }, DEFAULT_OOV_PROB)
    if clusters_loc:
        with msg.loading('Reading clusters...'):
            clusters = read_clusters(clusters_loc)
        msg.good('Read clusters')
    else:
        clusters = {
            
        }
    lex_attrs = []
    sorted_probs = sorted(probs.items(), key=(lambda item: item[1]), reverse=True)
    if len(sorted_probs):
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