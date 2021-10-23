

def roc_auc_score(y_true, y_score, average='macro', sample_weight=None, max_fpr=None):
    'Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC)\n    from prediction scores.\n\n    Note: this implementation is restricted to the binary classification task\n    or multilabel classification task in label indicator format.\n\n    Read more in the :ref:`User Guide <roc_metrics>`.\n\n    Parameters\n    ----------\n    y_true : array, shape = [n_samples] or [n_samples, n_classes]\n        True binary labels or binary label indicators.\n\n    y_score : array, shape = [n_samples] or [n_samples, n_classes]\n        Target scores, can either be probability estimates of the positive\n        class, confidence values, or non-thresholded measure of decisions\n        (as returned by "decision_function" on some classifiers). For binary\n        y_true, y_score is supposed to be the score of the class with greater\n        label.\n\n    average : string, [None, \'micro\', \'macro\' (default), \'samples\', \'weighted\']\n        If ``None``, the scores for each class are returned. Otherwise,\n        this determines the type of averaging performed on the data:\n\n        ``\'micro\'``:\n            Calculate metrics globally by considering each element of the label\n            indicator matrix as a label.\n        ``\'macro\'``:\n            Calculate metrics for each label, and find their unweighted\n            mean.  This does not take label imbalance into account.\n        ``\'weighted\'``:\n            Calculate metrics for each label, and find their average, weighted\n            by support (the number of true instances for each label).\n        ``\'samples\'``:\n            Calculate metrics for each instance, and find their average.\n\n        Will be ignored when ``y_true`` is binary.\n\n    sample_weight : array-like of shape = [n_samples], optional\n        Sample weights.\n\n    max_fpr : float > 0 and <= 1, optional\n        If not ``None``, the standardized partial AUC [3]_ over the range\n        [0, max_fpr] is returned.\n\n    Returns\n    -------\n    auc : float\n\n    References\n    ----------\n    .. [1] `Wikipedia entry for the Receiver operating characteristic\n            <https://en.wikipedia.org/wiki/Receiver_operating_characteristic>`_\n\n    .. [2] Fawcett T. An introduction to ROC analysis[J]. Pattern Recognition\n           Letters, 2006, 27(8):861-874.\n\n    .. [3] `Analyzing a portion of the ROC curve. McClish, 1989\n            <https://www.ncbi.nlm.nih.gov/pubmed/2668680>`_\n\n    See also\n    --------\n    average_precision_score : Area under the precision-recall curve\n\n    roc_curve : Compute Receiver operating characteristic (ROC) curve\n\n    Examples\n    --------\n    >>> import numpy as np\n    >>> from sklearn.metrics import roc_auc_score\n    >>> y_true = np.array([0, 0, 1, 1])\n    >>> y_scores = np.array([0.1, 0.4, 0.35, 0.8])\n    >>> roc_auc_score(y_true, y_scores)\n    0.75\n\n    '

    def _binary_roc_auc_score(y_true, y_score, sample_weight=None):
        if (len(np.unique(y_true)) != 2):
            raise ValueError('Only one class present in y_true. ROC AUC score is not defined in that case.')
        (fpr, tpr, _) = roc_curve(y_true, y_score, sample_weight=sample_weight)
        if ((max_fpr is None) or (max_fpr == 1)):
            return auc(fpr, tpr)
        if ((max_fpr <= 0) or (max_fpr > 1)):
            raise ValueError(('Expected max_fpr in range (0, 1], got: %r' % max_fpr))
        stop = np.searchsorted(fpr, max_fpr, 'right')
        x_interp = [fpr[(stop - 1)], fpr[stop]]
        y_interp = [tpr[(stop - 1)], tpr[stop]]
        tpr = np.append(tpr[:stop], np.interp(max_fpr, x_interp, y_interp))
        fpr = np.append(fpr[:stop], max_fpr)
        partial_auc = auc(fpr, tpr)
        min_area = (0.5 * (max_fpr ** 2))
        max_area = max_fpr
        return (0.5 * (1 + ((partial_auc - min_area) / (max_area - min_area))))
    y_type = type_of_target(y_true)
    if (y_type == 'binary'):
        labels = np.unique(y_true)
        y_true = label_binarize(y_true, labels)[:, 0]
    return _average_binary_score(_binary_roc_auc_score, y_true, y_score, average, sample_weight=sample_weight)
