def fetch_20newsgroups(data_home=None, subset='train', categories=None, shuffle=True, random_state=42, remove=(), download_if_missing=True):
    "Load the filenames and data from the 20 newsgroups dataset (classification).\n\n    Download it if necessary.\n\n    =================   ==========\n    Classes                     20\n    Samples total            18846\n    Dimensionality               1\n    Features                  text\n    =================   ==========\n\n    Read more in the :ref:`User Guide <20newsgroups_dataset>`.\n\n    Parameters\n    ----------\n    data_home : optional, default: None\n        Specify a download and cache folder for the datasets. If None,\n        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.\n\n    subset : 'train' or 'test', 'all', optional\n        Select the dataset to load: 'train' for the training set, 'test'\n        for the test set, 'all' for both, with shuffled ordering.\n\n    categories : None or collection of string or unicode\n        If None (default), load all the categories.\n        If not None, list of category names to load (other categories\n        ignored).\n\n    shuffle : bool, optional\n        Whether or not to shuffle the data: might be important for models that\n        make the assumption that the samples are independent and identically\n        distributed (i.i.d.), such as stochastic gradient descent.\n\n    random_state : int, RandomState instance or None (default)\n        Determines random number generation for dataset shuffling. Pass an int\n        for reproducible output across multiple function calls.\n        See :term:`Glossary <random_state>`.\n\n    remove : tuple\n        May contain any subset of ('headers', 'footers', 'quotes'). Each of\n        these are kinds of text that will be detected and removed from the\n        newsgroup posts, preventing classifiers from overfitting on\n        metadata.\n\n        'headers' removes newsgroup headers, 'footers' removes blocks at the\n        ends of posts that look like signatures, and 'quotes' removes lines\n        that appear to be quoting another post.\n\n        'headers' follows an exact standard; the other filters are not always\n        correct.\n\n    download_if_missing : optional, True by default\n        If False, raise an IOError if the data is not locally available\n        instead of trying to download the data from the source site.\n\n    Returns\n    -------\n    bunch : Bunch object\n        bunch.data: list, length [n_samples]\n        bunch.target: array, shape [n_samples]\n        bunch.filenames: list, length [n_classes]\n        bunch.DESCR: a description of the dataset.\n    "
    data_home = get_data_home(data_home=data_home)
    cache_path = _pkl_filepath(data_home, CACHE_NAME)
    twenty_home = os.path.join(data_home, '20news_home')
    cache = None
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                compressed_content = f.read()
            uncompressed_content = codecs.decode(compressed_content, 'zlib_codec')
            cache = pickle.loads(uncompressed_content)
        except Exception as e:
            print((80 * '_'))
            print('Cache loading failed')
            print((80 * '_'))
            print(e)
    if (cache is None):
        if download_if_missing:
            logger.info('Downloading 20news dataset. This may take a few minutes.')
            cache = _download_20newsgroups(target_dir=twenty_home, cache_path=cache_path)
        else:
            raise IOError('20Newsgroups dataset not found')
    if (subset in ('train', 'test')):
        data = cache[subset]
    elif (subset == 'all'):
        data_lst = list()
        target = list()
        filenames = list()
        for subset in ('train', 'test'):
            data = cache[subset]
            data_lst.extend(data.data)
            target.extend(data.target)
            filenames.extend(data.filenames)
        data.data = data_lst
        data.target = np.array(target)
        data.filenames = np.array(filenames)
    else:
        raise ValueError(("subset can only be 'train', 'test' or 'all', got '%s'" % subset))
    module_path = dirname(__file__)
    with open(join(module_path, 'descr', 'twenty_newsgroups.rst')) as rst_file:
        fdescr = rst_file.read()
    data.DESCR = fdescr
    if ('headers' in remove):
        data.data = [strip_newsgroup_header(text) for text in data.data]
    if ('footers' in remove):
        data.data = [strip_newsgroup_footer(text) for text in data.data]
    if ('quotes' in remove):
        data.data = [strip_newsgroup_quoting(text) for text in data.data]
    if (categories is not None):
        labels = [(data.target_names.index(cat), cat) for cat in categories]
        labels.sort()
        (labels, categories) = zip(*labels)
        mask = np.in1d(data.target, labels)
        data.filenames = data.filenames[mask]
        data.target = data.target[mask]
        data.target = np.searchsorted(labels, data.target)
        data.target_names = list(categories)
        data_lst = np.array(data.data, dtype=object)
        data_lst = data_lst[mask]
        data.data = data_lst.tolist()
    if shuffle:
        random_state = check_random_state(random_state)
        indices = np.arange(data.target.shape[0])
        random_state.shuffle(indices)
        data.filenames = data.filenames[indices]
        data.target = data.target[indices]
        data_lst = np.array(data.data, dtype=object)
        data_lst = data_lst[indices]
        data.data = data_lst.tolist()
    return data