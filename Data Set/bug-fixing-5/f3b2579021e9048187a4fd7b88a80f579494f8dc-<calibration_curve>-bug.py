def calibration_curve(y_true, y_prob, normalize=False, n_bins=5):
    'Compute true and predicted probabilities for a calibration curve.\n\n     The method assumes the inputs come from a binary classifier.\n\n     Calibration curves may also be referred to as reliability diagrams.\n\n    Read more in the :ref:`User Guide <calibration>`.\n\n    Parameters\n    ----------\n    y_true : array, shape (n_samples,)\n        True targets.\n\n    y_prob : array, shape (n_samples,)\n        Probabilities of the positive class.\n\n    normalize : bool, optional, default=False\n        Whether y_prob needs to be normalized into the bin [0, 1], i.e. is not\n        a proper probability. If True, the smallest value in y_prob is mapped\n        onto 0 and the largest one onto 1.\n\n    n_bins : int\n        Number of bins. A bigger number requires more data.\n\n    Returns\n    -------\n    prob_true : array, shape (n_bins,)\n        The true probability in each bin (fraction of positives).\n\n    prob_pred : array, shape (n_bins,)\n        The mean predicted probability in each bin.\n\n    References\n    ----------\n    Alexandru Niculescu-Mizil and Rich Caruana (2005) Predicting Good\n    Probabilities With Supervised Learning, in Proceedings of the 22nd\n    International Conference on Machine Learning (ICML).\n    See section 4 (Qualitative Analysis of Predictions).\n    '
    y_true = column_or_1d(y_true)
    y_prob = column_or_1d(y_prob)
    if normalize:
        y_prob = ((y_prob - y_prob.min()) / (y_prob.max() - y_prob.min()))
    elif ((y_prob.min() < 0) or (y_prob.max() > 1)):
        raise ValueError('y_prob has values outside [0, 1] and normalize is set to False.')
    y_true = _check_binary_probabilistic_predictions(y_true, y_prob)
    bins = np.linspace(0.0, (1.0 + 1e-08), (n_bins + 1))
    binids = (np.digitize(y_prob, bins) - 1)
    bin_sums = np.bincount(binids, weights=y_prob, minlength=len(bins))
    bin_true = np.bincount(binids, weights=y_true, minlength=len(bins))
    bin_total = np.bincount(binids, minlength=len(bins))
    nonzero = (bin_total != 0)
    prob_true = (bin_true[nonzero] / bin_total[nonzero])
    prob_pred = (bin_sums[nonzero] / bin_total[nonzero])
    return (prob_true, prob_pred)