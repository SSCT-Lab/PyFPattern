def read_dbpedia(tf, split, shrink=1, char_based=False):
    dataset = []
    f = tf.extractfile('dbpedia_csv/{}.csv'.format(split))
    if (sys.version_info > (3, 0)):
        f = io.TextIOWrapper(f, encoding='utf-8')
    for (i, (label, title, text)) in enumerate(csv.reader(f)):
        if ((i % shrink) != 0):
            continue
        label = (int(label) - 1)
        tokens = split_text(normalize_text(text), char_based)
        dataset.append((tokens, label))
    return dataset