@classmethod
def train(cls, wr_path, corpus_file, out_path, size=100, window=15, symmetric=1, min_count=5, max_vocab_size=0, sgd_num=100, lrate=0.001, period=10, iter=90, epsilon=0.75, dump_period=10, reg=0, alpha=100, beta=99, loss='hinge', memory=4.0, cleanup_files=True, sorted_vocab=1, ensemble=0):
    '\n        `wr_path` is the path to the Wordrank directory.\n        `corpus_file` is the filename of the text file to be used for training the Wordrank model.\n        Expects file to contain space-separated tokens in a single line\n        `out_path` is the path to directory which will be created to save embeddings and training data.\n        `size` is the dimensionality of the feature vectors.\n        `window` is the number of context words to the left (and to the right, if symmetric = 1).\n        `symmetric` if 0, only use left context words, else use left and right both.\n        `min_count` = ignore all words with total frequency lower than this.\n        `max_vocab_size` upper bound on vocabulary size, i.e. keep the <int> most frequent words. Default is 0 for no limit.\n        `sgd_num` number of SGD taken for each data point.\n        `lrate` is the learning rate (too high diverges, give Nan).\n        `period` is the period of xi variable updates\n        `iter` = number of iterations (epochs) over the corpus.\n        `epsilon` is the power scaling value for weighting function.\n        `dump_period` is the period after which embeddings should be dumped.\n        `reg` is the value of regularization parameter.\n        `alpha` is the alpha parameter of gamma distribution.\n        `beta` is the beta parameter of gamma distribution.\n        `loss` = name of the loss (logistic, hinge).\n        `memory` = soft limit for memory consumption, in GB.\n        `cleanup_files` if True, delete directory and files used by this wrapper, setting to False can be useful for debugging\n        `sorted_vocab` = if 1 (default), sort the vocabulary by descending frequency before assigning word indexes.\n        `ensemble` = 0 (default), use ensemble of word and context vectors\n        '
    meta_data_path = 'matrix.meta'
    vocab_file = 'vocab.txt'
    temp_vocab_file = 'tempvocab.txt'
    cooccurrence_file = 'cooccurrence'
    cooccurrence_shuf_file = 'wiki.toy'
    meta_file = 'meta'
    model_dir = os.path.join(wr_path, out_path)
    meta_dir = os.path.join(model_dir, 'meta')
    os.makedirs(meta_dir)
    logger.info("Dumped data will be stored in '%s'", model_dir)
    copyfile(corpus_file, os.path.join(meta_dir, corpus_file.split('/')[(- 1)]))
    os.chdir(meta_dir)
    cmd_vocab_count = ['../../glove/vocab_count', '-min-count', str(min_count), '-max-vocab', str(max_vocab_size)]
    cmd_cooccurence_count = ['../../glove/cooccur', '-memory', str(memory), '-vocab-file', temp_vocab_file, '-window-size', str(window), '-symmetric', str(symmetric)]
    cmd_shuffle_cooccurences = ['../../glove/shuffle', '-memory', str(memory)]
    cmd_del_vocab_freq = ['cut', '-d', ' ', '-f', '1', temp_vocab_file]
    commands = [cmd_vocab_count, cmd_cooccurence_count, cmd_shuffle_cooccurences]
    logger.info("Prepare training data using glove code '%s'", commands)
    input_fnames = [corpus_file.split('/')[(- 1)], corpus_file.split('/')[(- 1)], cooccurrence_file]
    output_fnames = [temp_vocab_file, cooccurrence_file, cooccurrence_shuf_file]
    for (command, input_fname, output_fname) in zip(commands, input_fnames, output_fnames):
        with smart_open(input_fname, 'rb') as r:
            with smart_open(output_fname, 'wb') as w:
                utils.check_output(w, args=command, stdin=r)
    with smart_open(vocab_file, 'wb') as w:
        utils.check_output(w, args=cmd_del_vocab_freq)
    with smart_open(vocab_file, 'rb') as f:
        numwords = sum((1 for line in f))
    with smart_open(cooccurrence_shuf_file, 'rb') as f:
        numlines = sum((1 for line in f))
    with smart_open(meta_file, 'wb') as f:
        meta_info = '{0} {1}\n{2} {3}\n{4} {5}'.format(numwords, numwords, numlines, cooccurrence_shuf_file, numwords, vocab_file)
        f.write(meta_info.encode('utf-8'))
    if ((iter % dump_period) == 0):
        iter += 1
    else:
        logger.warning('Resultant embedding would be from %d iteration', (iter - (iter % dump_period)))
    wr_args = {
        'path': 'meta',
        'nthread': multiprocessing.cpu_count(),
        'sgd_num': sgd_num,
        'lrate': lrate,
        'period': period,
        'iter': iter,
        'epsilon': epsilon,
        'dump_prefix': 'model',
        'dump_period': dump_period,
        'dim': size,
        'reg': reg,
        'alpha': alpha,
        'beta': beta,
        'loss': loss,
    }
    os.chdir('..')
    cmd = ['mpirun', '-np', '1', '../wordrank']
    for (option, value) in wr_args.items():
        cmd.append(('--%s' % option))
        cmd.append(str(value))
    logger.info("Running wordrank binary '%s'", cmd)
    output = utils.check_output(args=cmd)
    max_iter_dump = (iter - (iter % dump_period))
    copyfile(('model_word_%d.txt' % max_iter_dump), 'wordrank.words')
    copyfile(('model_context_%d.txt' % max_iter_dump), 'wordrank.contexts')
    model = cls.load_wordrank_model('wordrank.words', os.path.join('meta', vocab_file), 'wordrank.contexts', sorted_vocab, ensemble)
    os.chdir('../..')
    if cleanup_files:
        rmtree(model_dir)
    return model