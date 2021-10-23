def get_word_index(path='reuters_word_index.pkl'):
    path = get_file(path, origin='https://s3.amazonaws.com/text-datasets/reuters_word_index.pkl')
    f = open(path, 'rb')
    if (sys.version_info < (3,)):
        data = cPickle.load(f)
    else:
        data = cPickle.load(f, encoding='latin1')
    f.close()
    return data