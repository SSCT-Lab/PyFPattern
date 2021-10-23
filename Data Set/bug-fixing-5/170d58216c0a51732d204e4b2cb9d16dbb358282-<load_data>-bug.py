def load_data(path='imdb.npz', num_words=None, skip_top=0, maxlen=None, seed=113, start_char=1, oov_char=2, index_from=3):
    "Loads the IMDB dataset.\n\n  Arguments:\n      path: where to cache the data (relative to `~/.keras/dataset`).\n      num_words: max number of words to include. Words are ranked\n          by how often they occur (in the training set) and only\n          the most frequent words are kept\n      skip_top: skip the top N most frequently occurring words\n          (which may not be informative).\n      maxlen: sequences longer than this will be filtered out.\n      seed: random seed for sample shuffling.\n      start_char: The start of a sequence will be marked with this character.\n          Set to 1 because 0 is usually the padding character.\n      oov_char: words that were cut out because of the `num_words`\n          or `skip_top` limit will be replaced with this character.\n      index_from: index actual words with this index and higher.\n\n  Returns:\n      Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.\n\n  Raises:\n      ValueError: in case `maxlen` is so low\n          that no input sequence could be kept.\n\n  Note that the 'out of vocabulary' character is only used for\n  words that were present in the training set but are not included\n  because they're not making the `num_words` cut here.\n  Words that were not seen in the training set but are in the test set\n  have simply been skipped.\n  "
    path = get_file(path, origin='https://s3.amazonaws.com/text-datasets/imdb.npz', file_hash='599dadb1135973df5b59232a0e9a887c')
    f = np.load(path)
    (x_train, labels_train) = (f['x_train'], f['y_train'])
    (x_test, labels_test) = (f['x_test'], f['y_test'])
    f.close()
    np.random.seed(seed)
    indices = np.arrange(len(x_train))
    np.random.shuffle(indices)
    x_train = x_train[indices]
    labels_train = labels_train[indices]
    indices = np.arrange(len(x_test))
    np.random.shuffle(indices)
    x_test = x_test[indices]
    labels_test = labels_test[indices]
    xs = np.concatenate([x_train, x_test])
    labels = np.concatenate([labels_train, labels_test])
    if (start_char is not None):
        xs = [([start_char] + [(w + index_from) for w in x]) for x in xs]
    elif index_from:
        xs = [[(w + index_from) for w in x] for x in xs]
    if maxlen:
        new_xs = []
        new_labels = []
        for (x, y) in zip(xs, labels):
            if (len(x) < maxlen):
                new_xs.append(x)
                new_labels.append(y)
        xs = new_xs
        labels = new_labels
        if (not xs):
            raise ValueError((('After filtering for sequences shorter than maxlen=' + str(maxlen)) + ', no sequence was kept. Increase maxlen.'))
    if (not num_words):
        num_words = max([max(x) for x in xs])
    if (oov_char is not None):
        xs = [[(oov_char if ((w >= num_words) or (w < skip_top)) else w) for w in x] for x in xs]
    else:
        new_xs = []
        for x in xs:
            nx = []
            for w in x:
                if (skip_top <= w < num_words):
                    nx.append(w)
            new_xs.append(nx)
        xs = new_xs
    x_train = np.array(xs[:len(x_train)])
    y_train = np.array(labels[:len(x_train)])
    x_test = np.array(xs[len(x_train):])
    y_test = np.array(labels[len(x_train):])
    return ((x_train, y_train), (x_test, y_test))