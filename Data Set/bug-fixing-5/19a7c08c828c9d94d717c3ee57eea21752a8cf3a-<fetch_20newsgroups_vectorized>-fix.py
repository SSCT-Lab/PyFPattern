def fetch_20newsgroups_vectorized(subset='train', remove=(), data_home=None, download_if_missing=True, return_X_y=False):
    "Load the 20 newsgroups dataset and vectorize it into token counts (classification).\n\n    Download it if necessary.\n\n    This is a convenience function; the transformation is done using the\n    default settings for\n    :class:`sklearn.feature_extraction.text.CountVectorizer`. For more\n    advanced usage (stopword filtering, n-gram extraction, etc.), combine\n    fetch_20newsgroups with a custom\n    :class:`sklearn.feature_extraction.text.CountVectorizer`,\n    :class:`sklearn.feature_extraction.text.HashingVectorizer`,\n    :class:`sklearn.feature_extraction.text.TfidfTransformer` or\n    :class:`sklearn.feature_extraction.text.TfidfVectorizer`.\n\n    =================   ==========\n    Classes                     20\n    Samples total            18846\n    Dimensionality          130107\n    Features                  real\n    =================   ==========\n\n    Read more in the :ref:`User Guide <20newsgroups_dataset>`.\n\n    Parameters\n    ----------\n    subset : 'train' or 'test', 'all', optional\n        Select the dataset to load: 'train' for the training set, 'test'\n        for the test set, 'all' for both, with shuffled ordering.\n\n    remove : tuple\n        May contain any subset of ('headers', 'footers', 'quotes'). Each of\n        these are kinds of text that will be detected and removed from the\n        newsgroup posts, preventing classifiers from overfitting on\n        metadata.\n\n        'headers' removes newsgroup headers, 'footers' removes blocks at the\n        ends of posts that look like signatures, and 'quotes' removes lines\n        that appear to be quoting another post.\n\n    data_home : optional, default: None\n        Specify an download and cache folder for the datasets. If None,\n        all scikit-learn data is stored in '~/scikit_learn_data' subfolders.\n\n    download_if_missing : optional, True by default\n        If False, raise an IOError if the data is not locally available\n        instead of trying to download the data from the source site.\n\n    return_X_y : boolean, default=False.\n        If True, returns ``(data.data, data.target)`` instead of a Bunch\n        object.\n\n        .. versionadded:: 0.20\n\n    Returns\n    -------\n    bunch : Bunch object with the following attribute:\n        - bunch.data: sparse matrix, shape [n_samples, n_features]\n        - bunch.target: array, shape [n_samples]\n        - bunch.target_names: a list of categories of the returned data,\n          length [n_classes].\n        - bunch.DESCR: a description of the dataset.\n\n    (data, target) : tuple if ``return_X_y`` is True\n\n        .. versionadded:: 0.20\n    "
    data_home = get_data_home(data_home=data_home)
    filebase = '20newsgroup_vectorized'
    if remove:
        filebase += ('remove-' + '-'.join(remove))
    target_file = _pkl_filepath(data_home, (filebase + '.pkl'))
    data_train = fetch_20newsgroups(data_home=data_home, subset='train', categories=None, shuffle=True, random_state=12, remove=remove, download_if_missing=download_if_missing)
    data_test = fetch_20newsgroups(data_home=data_home, subset='test', categories=None, shuffle=True, random_state=12, remove=remove, download_if_missing=download_if_missing)
    if os.path.exists(target_file):
        (X_train, X_test) = _joblib.load(target_file)
    else:
        vectorizer = CountVectorizer(dtype=np.int16)
        X_train = vectorizer.fit_transform(data_train.data).tocsr()
        X_test = vectorizer.transform(data_test.data).tocsr()
        _joblib.dump((X_train, X_test), target_file, compress=9)
    X_train = X_train.astype(np.float64)
    X_test = X_test.astype(np.float64)
    normalize(X_train, copy=False)
    normalize(X_test, copy=False)
    target_names = data_train.target_names
    if (subset == 'train'):
        data = X_train
        target = data_train.target
    elif (subset == 'test'):
        data = X_test
        target = data_test.target
    elif (subset == 'all'):
        data = sp.vstack((X_train, X_test)).tocsr()
        target = np.concatenate((data_train.target, data_test.target))
    else:
        raise ValueError(("%r is not a valid subset: should be one of ['train', 'test', 'all']" % subset))
    module_path = dirname(__file__)
    with open(join(module_path, 'descr', 'twenty_newsgroups.rst')) as rst_file:
        fdescr = rst_file.read()
    if return_X_y:
        return (data, target)
    return Bunch(data=data, target=target, target_names=target_names, DESCR=fdescr)