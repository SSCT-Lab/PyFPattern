def create_vocabulary(vocabulary_path, data_path, max_vocabulary_size, tokenizer=None, normalize_digits=True):
    'Create vocabulary file (if it does not exist yet) from data file.\n\n  Data file is assumed to contain one sentence per line. Each sentence is\n  tokenized and digits are normalized (if normalize_digits is set).\n  Vocabulary contains the most-frequent tokens up to max_vocabulary_size.\n  We write it to vocabulary_path in a one-token-per-line format, so that later\n  token in the first line gets id=0, second line gets id=1, and so on.\n\n  Args:\n    vocabulary_path: path where the vocabulary will be created.\n    data_path: data file that will be used to create vocabulary.\n    max_vocabulary_size: limit on the size of the created vocabulary.\n    tokenizer: a function to use to tokenize each data sentence;\n      if None, basic_tokenizer will be used.\n    normalize_digits: Boolean; if true, all digits are replaced by 0s.\n  '
    if (not gfile.Exists(vocabulary_path)):
        print(('Creating vocabulary %s from data %s' % (vocabulary_path, data_path)))
        vocab = {
            
        }
        with gfile.GFile(data_path, mode='rb') as f:
            counter = 0
            for line in f:
                counter += 1
                if ((counter % 100000) == 0):
                    print(('  processing line %d' % counter))
                line = tf.compat.as_bytes(line)
                tokens = (tokenizer(line) if tokenizer else basic_tokenizer(line))
                for w in tokens:
                    word = (_DIGIT_RE.sub(b'0', w) if normalize_digits else w)
                    if (word in vocab):
                        vocab[word] += 1
                    else:
                        vocab[word] = 1
            vocab_list = (_START_VOCAB + sorted(vocab, key=vocab.get, reverse=True))
            if (len(vocab_list) > max_vocabulary_size):
                vocab_list = vocab_list[:max_vocabulary_size]
            with gfile.GFile(vocabulary_path, mode='wb') as vocab_file:
                for w in vocab_list:
                    vocab_file.write((w + b'\n'))