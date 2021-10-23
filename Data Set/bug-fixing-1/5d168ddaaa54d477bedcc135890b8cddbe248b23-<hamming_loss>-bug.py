

def hamming_loss(y_true, y_pred, labels=None, sample_weight=None):
    "Compute the average Hamming loss.\n\n    The Hamming loss is the fraction of labels that are incorrectly predicted.\n\n    Read more in the :ref:`User Guide <hamming_loss>`.\n\n    Parameters\n    ----------\n    y_true : 1d array-like, or label indicator array / sparse matrix\n        Ground truth (correct) labels.\n\n    y_pred : 1d array-like, or label indicator array / sparse matrix\n        Predicted labels, as returned by a classifier.\n\n    labels : array, shape = [n_labels], optional (default='deprecated')\n        Integer array of labels. If not provided, labels will be inferred\n        from y_true and y_pred.\n\n        .. versionadded:: 0.18\n        .. deprecated:: 0.21\n           This parameter ``labels`` is deprecated in version 0.21 and will\n           be removed in version 0.23. Hamming loss uses ``y_true.shape[1]``\n           for the number of labels when y_true is binary label indicators,\n           so it is unnecessary for the user to specify.\n\n    sample_weight : array-like of shape = [n_samples], optional\n        Sample weights.\n\n        .. versionadded:: 0.18\n\n    Returns\n    -------\n    loss : float or int,\n        Return the average Hamming loss between element of ``y_true`` and\n        ``y_pred``.\n\n    See Also\n    --------\n    accuracy_score, jaccard_score, zero_one_loss\n\n    Notes\n    -----\n    In multiclass classification, the Hamming loss corresponds to the Hamming\n    distance between ``y_true`` and ``y_pred`` which is equivalent to the\n    subset ``zero_one_loss`` function.\n\n    In multilabel classification, the Hamming loss is different from the\n    subset zero-one loss. The zero-one loss considers the entire set of labels\n    for a given sample incorrect if it does entirely match the true set of\n    labels. Hamming loss is more forgiving in that it penalizes the individual\n    labels.\n\n    The Hamming loss is upperbounded by the subset zero-one loss. When\n    normalized over samples, the Hamming loss is always between 0 and 1.\n\n    References\n    ----------\n    .. [1] Grigorios Tsoumakas, Ioannis Katakis. Multi-Label Classification:\n           An Overview. International Journal of Data Warehousing & Mining,\n           3(3), 1-13, July-September 2007.\n\n    .. [2] `Wikipedia entry on the Hamming distance\n           <https://en.wikipedia.org/wiki/Hamming_distance>`_\n\n    Examples\n    --------\n    >>> from sklearn.metrics import hamming_loss\n    >>> y_pred = [1, 2, 3, 4]\n    >>> y_true = [2, 2, 3, 4]\n    >>> hamming_loss(y_true, y_pred)\n    0.25\n\n    In the multilabel case with binary label indicators:\n\n    >>> import numpy as np\n    >>> hamming_loss(np.array([[0, 1], [1, 1]]), np.zeros((2, 2)))\n    0.75\n    "
    (y_type, y_true, y_pred) = _check_targets(y_true, y_pred)
    check_consistent_length(y_true, y_pred, sample_weight)
    if (labels is not None):
        warnings.warn('The labels parameter is unused. It was deprecated in version 0.21 and will be removed in version 0.23', DeprecationWarning)
    if (sample_weight is None):
        weight_average = 1.0
    else:
        weight_average = np.mean(sample_weight)
    if y_type.startswith('multilabel'):
        n_differences = count_nonzero((y_true - y_pred), sample_weight=sample_weight)
        return (n_differences / ((y_true.shape[0] * y_true.shape[1]) * weight_average))
    elif (y_type in ['binary', 'multiclass']):
        return _weighted_sum((y_true != y_pred), sample_weight, normalize=True)
    else:
        raise ValueError('{0} is not supported'.format(y_type))
