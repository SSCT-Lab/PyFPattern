def fetch_kddcup99(subset=None, shuffle=False, random_state=None, percent10=True, download_if_missing=True):
    "Load and return the kddcup 99 dataset (classification).\n\n    The KDD Cup '99 dataset was created by processing the tcpdump portions\n    of the 1998 DARPA Intrusion Detection System (IDS) Evaluation dataset,\n    created by MIT Lincoln Lab [1]. The artificial data was generated using\n    a closed network and hand-injected attacks to produce a large number of\n    different types of attack with normal activity in the background.\n    As the initial goal was to produce a large training set for supervised\n    learning algorithms, there is a large proportion (80.1%) of abnormal\n    data which is unrealistic in real world, and inappropriate for unsupervised\n    anomaly detection which aims at detecting 'abnormal' data, ie\n\n    1) qualitatively different from normal data.\n\n    2) in large minority among the observations.\n\n    We thus transform the KDD Data set into two different data sets: SA and SF.\n\n    - SA is obtained by simply selecting all the normal data, and a small\n      proportion of abnormal data to gives an anomaly proportion of 1%.\n\n    - SF is obtained as in [2]\n      by simply picking up the data whose attribute logged_in is positive, thus\n      focusing on the intrusion attack, which gives a proportion of 0.3% of\n      attack.\n\n    - http and smtp are two subsets of SF corresponding with third feature\n      equal to 'http' (resp. to 'smtp')\n\n\n    General KDD structure :\n\n    ================      ==========================================\n    Samples total         4898431\n    Dimensionality        41\n    Features              discrete (int) or continuous (float)\n    Targets               str, 'normal.' or name of the anomaly type\n    ================      ==========================================\n\n    SA structure :\n\n    ================      ==========================================\n    Samples total         976158\n    Dimensionality        41\n    Features              discrete (int) or continuous (float)\n    Targets               str, 'normal.' or name of the anomaly type\n    ================      ==========================================\n\n    SF structure :\n\n    ================      ==========================================\n    Samples total         699691\n    Dimensionality        4\n    Features              discrete (int) or continuous (float)\n    Targets               str, 'normal.' or name of the anomaly type\n    ================      ==========================================\n\n    http structure :\n\n    ================      ==========================================\n    Samples total         619052\n    Dimensionality        3\n    Features              discrete (int) or continuous (float)\n    Targets               str, 'normal.' or name of the anomaly type\n    ================      ==========================================\n\n    smtp structure :\n\n    ================      ==========================================\n    Samples total         95373\n    Dimensionality        3\n    Features              discrete (int) or continuous (float)\n    Targets               str, 'normal.' or name of the anomaly type\n    ================      ==========================================\n\n    .. versionadded:: 0.18\n\n    Parameters\n    ----------\n    subset : None, 'SA', 'SF', 'http', 'smtp'\n        To return the corresponding classical subsets of kddcup 99.\n        If None, return the entire kddcup 99 dataset.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        Random state for shuffling the dataset.\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.\n\n    shuffle : bool, default=False\n        Whether to shuffle dataset.\n\n    percent10 : bool, default=True\n        Whether to load only 10 percent of the data.\n\n    download_if_missing : bool, default=True\n        If False, raise a IOError if the data is not locally available\n        instead of trying to download the data from the source site.\n\n    Returns\n    -------\n    data : Bunch\n        Dictionary-like object, the interesting attributes are:\n        'data', the data to learn and 'target', the regression target for each\n        sample.\n\n\n    References\n    ----------\n    .. [1] Analysis and Results of the 1999 DARPA Off-Line Intrusion\n           Detection Evaluation Richard Lippmann, Joshua W. Haines,\n           David J. Fried, Jonathan Korba, Kumar Das\n\n    .. [2] K. Yamanishi, J.-I. Takeuchi, G. Williams, and P. Milne. Online\n           unsupervised outlier detection using finite mixtures with\n           discounting learning algorithms. In Proceedings of the sixth\n           ACM SIGKDD international conference on Knowledge discovery\n           and data mining, pages 320-324. ACM Press, 2000.\n\n    "
    kddcup99 = _fetch_brute_kddcup99(shuffle=shuffle, percent10=percent10, download_if_missing=download_if_missing)
    data = kddcup99.data
    target = kddcup99.target
    if (subset == 'SA'):
        s = (target == b'normal.')
        t = np.logical_not(s)
        normal_samples = data[s, :]
        normal_targets = target[s]
        abnormal_samples = data[t, :]
        abnormal_targets = target[t]
        n_samples_abnormal = abnormal_samples.shape[0]
        random_state = check_random_state(random_state)
        r = random_state.randint(0, n_samples_abnormal, 3377)
        abnormal_samples = abnormal_samples[r]
        abnormal_targets = abnormal_targets[r]
        data = np.r_[(normal_samples, abnormal_samples)]
        target = np.r_[(normal_targets, abnormal_targets)]
    if ((subset == 'SF') or (subset == 'http') or (subset == 'smtp')):
        s = (data[:, 11] == 1)
        data = np.c_[(data[s, :11], data[s, 12:])]
        target = target[s]
        data[:, 0] = np.log((data[:, 0] + 0.1).astype(float))
        data[:, 4] = np.log((data[:, 4] + 0.1).astype(float))
        data[:, 5] = np.log((data[:, 5] + 0.1).astype(float))
        if (subset == 'http'):
            s = (data[:, 2] == b'http')
            data = data[s]
            target = target[s]
            data = np.c_[(data[:, 0], data[:, 4], data[:, 5])]
        if (subset == 'smtp'):
            s = (data[:, 2] == b'smtp')
            data = data[s]
            target = target[s]
            data = np.c_[(data[:, 0], data[:, 4], data[:, 5])]
        if (subset == 'SF'):
            data = np.c_[(data[:, 0], data[:, 2], data[:, 4], data[:, 5])]
    return Bunch(data=data, target=target)