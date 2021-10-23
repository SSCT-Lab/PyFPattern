

def roc_auc_score(y_true, y_score, average='macro', sample_weight=None, max_fpr=None, multi_class='raise', labels=None):
    'Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC)\n    from prediction scores.\n\n    Note: this implementation is restricted to the binary classification task\n    or multilabel classification task in label indicator format.\n\n    Read more in the :ref:`User Guide <roc_metrics>`.\n\n    Parameters\n    ----------\n    y_true : array, shape = [n_samples] or [n_samples, n_classes]\n        True binary labels or binary label indicators.\n        The multiclass case expects shape = [n_samples] and labels\n        with values in ``range(n_classes)``.\n\n    y_score : array, shape = [n_samples] or [n_samples, n_classes]\n        Target scores, can either be probability estimates of the positive\n        class, confidence values, or non-thresholded measure of decisions\n        (as returned by "decision_function" on some classifiers). For binary\n        y_true, y_score is supposed to be the score of the class with greater\n        label. The multiclass case expects shape = [n_samples, n_classes]\n        where the scores correspond to probability estimates.\n\n    average : string, [None, \'micro\', \'macro\' (default), \'samples\', \'weighted\']\n        If ``None``, the scores for each class are returned. Otherwise,\n        this determines the type of averaging performed on the data:\n        Note: multiclass ROC AUC currently only handles the \'macro\' and\n        \'weighted\' averages.\n\n        ``\'micro\'``:\n            Calculate metrics globally by considering each element of the label\n            indicator matrix as a label.\n        ``\'macro\'``:\n            Calculate metrics for each label, and find their unweighted\n            mean.  This does not take label imbalance into account.\n        ``\'weighted\'``:\n            Calculate metrics for each label, and find their average, weighted\n            by support (the number of true instances for each label).\n        ``\'samples\'``:\n            Calculate metrics for each instance, and find their average.\n\n        Will be ignored when ``y_true`` is binary.\n\n    sample_weight : array-like of shape = [n_samples], optional\n        Sample weights.\n\n    max_fpr : float > 0 and <= 1, optional\n        If not ``None``, the standardized partial AUC [3]_ over the range\n        [0, max_fpr] is returned. For the multiclass case, ``max_fpr``,\n        should be either equal to ``None`` or ``1.0`` as AUC ROC partial\n        computation currently is not supported for multiclass.\n\n    multi_class : string, \'ovr\' or \'ovo\', optional(default=\'raise\')\n        Determines the type of multiclass configuration to use.\n        ``multi_class`` must be provided when ``y_true`` is multiclass.\n\n        ``\'ovr\'``:\n            Calculate metrics for the multiclass case using the one-vs-rest\n            approach.\n        ``\'ovo\'``:\n            Calculate metrics for the multiclass case using the one-vs-one\n            approach.\n\n    labels : array, shape = [n_classes] or None, optional (default=None)\n        List of labels to index ``y_score`` used for multiclass. If ``None``,\n        the lexicon order of ``y_true`` is used to index ``y_score``.\n\n    Returns\n    -------\n    auc : float\n\n    References\n    ----------\n    .. [1] `Wikipedia entry for the Receiver operating characteristic\n            <https://en.wikipedia.org/wiki/Receiver_operating_characteristic>`_\n\n    .. [2] Fawcett T. An introduction to ROC analysis[J]. Pattern Recognition\n           Letters, 2006, 27(8):861-874.\n\n    .. [3] `Analyzing a portion of the ROC curve. McClish, 1989\n            <https://www.ncbi.nlm.nih.gov/pubmed/2668680>`_\n\n    See also\n    --------\n    average_precision_score : Area under the precision-recall curve\n\n    roc_curve : Compute Receiver operating characteristic (ROC) curve\n\n    Examples\n    --------\n    >>> import numpy as np\n    >>> from sklearn.metrics import roc_auc_score\n    >>> y_true = np.array([0, 0, 1, 1])\n    >>> y_scores = np.array([0.1, 0.4, 0.35, 0.8])\n    >>> roc_auc_score(y_true, y_scores)\n    0.75\n\n    '
    y_type = type_of_target(y_true)
    y_true = check_array(y_true, ensure_2d=False, dtype=None)
    y_score = check_array(y_score, ensure_2d=False)
    if ((y_type == 'multiclass') or ((y_type == 'binary') and (y_score.ndim == 2) and (y_score.shape[1] > 2))):
        if ((max_fpr is not None) and (max_fpr != 1.0)):
            raise ValueError("Partial AUC computation not available in multiclass setting, 'max_fpr' must be set to `None`, received `max_fpr={0}` instead".format(max_fpr))
        if (multi_class == 'raise'):
            raise ValueError("multi_class must be in ('ovo', 'ovr')")
        return _multiclass_roc_auc_score(y_true, y_score, labels, multi_class, average, sample_weight)
    elif (y_type == 'binary'):
        labels = np.unique(y_true)
        y_true = label_binarize(y_true, labels)[:, 0]
        return _average_binary_score(partial(_binary_roc_auc_score, max_fpr=max_fpr), y_true, y_score, average, sample_weight=sample_weight)
    else:
        return _average_binary_score(partial(_binary_roc_auc_score, max_fpr=max_fpr), y_true, y_score, average, sample_weight=sample_weight)