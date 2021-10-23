def read_dbpedia(tf, split, shrink=1, char_based=False):
    dataset = []
    f = tf.extractfile('dbpedia_csv/{}.csv'.format(split))
    for (i, (label, title, text)) in enumerate(csv.reader(f)):
        if ((i % shrink) != 0):
            continue
        label = (int(label) - 1)
        tokens = split_text(normalize_text(text), char_based)
        dataset.append((tokens, label))
    return dataset