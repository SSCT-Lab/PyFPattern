def mean_tweedie_deviance(y_true, y_pred, sample_weight=None, p=0):
    'Mean Tweedie deviance regression loss.\n\n    Read more in the :ref:`User Guide <mean_tweedie_deviance>`.\n\n    Parameters\n    ----------\n    y_true : array-like of shape (n_samples,)\n        Ground truth (correct) target values.\n\n    y_pred : array-like of shape (n_samples,)\n        Estimated target values.\n\n    sample_weight : array-like, shape (n_samples,), optional\n        Sample weights.\n\n    p : float, optional\n        Tweedie power parameter. Either p ≤ 0 or p ≥ 1.\n\n        The higher `p` the less weight is given to extreme\n        deviations between true and predicted targets.\n\n        - p < 0: Extreme stable distribution. Requires: y_pred > 0.\n        - p = 0 : Normal distribution, output corresponds to\n          mean_squared_error. y_true and y_pred can be any real numbers.\n        - p = 1 : Poisson distribution. Requires: y_true ≥ 0 and y_pred > 0.\n        - 1 < p < 2 : Compound Poisson distribution. Requires: y_true ≥ 0\n          and y_pred > 0.\n        - p = 2 : Gamma distribution. Requires: y_true > 0 and y_pred > 0.\n        - p = 3 : Inverse Gaussian distribution. Requires: y_true > 0\n          and y_pred > 0.\n        - otherwise : Positive stable distribution. Requires: y_true > 0\n          and y_pred > 0.\n\n    Returns\n    -------\n    loss : float\n        A non-negative floating point value (the best value is 0.0).\n\n    Examples\n    --------\n    >>> from sklearn.metrics import mean_tweedie_deviance\n    >>> y_true = [2, 0, 1, 4]\n    >>> y_pred = [0.5, 0.5, 2., 2.]\n    >>> mean_tweedie_deviance(y_true, y_pred, p=1)\n    1.4260...\n    '
    (y_type, y_true, y_pred, _) = _check_reg_targets(y_true, y_pred, None, dtype=[np.float64, np.float32])
    if (y_type == 'continuous-multioutput'):
        raise ValueError('Multioutput not supported in mean_tweedie_deviance')
    check_consistent_length(y_true, y_pred, sample_weight)
    if (sample_weight is not None):
        sample_weight = column_or_1d(sample_weight)
        sample_weight = sample_weight[:, np.newaxis]
    message = 'Mean Tweedie deviance error with p={} can only be used on '.format(p)
    if (p < 0):
        if (y_pred <= 0).any():
            raise ValueError((message + 'strictly positive y_pred.'))
        dev = (2 * (((np.power(np.maximum(y_true, 0), (2 - p)) / ((1 - p) * (2 - p))) - ((y_true * np.power(y_pred, (1 - p))) / (1 - p))) + (np.power(y_pred, (2 - p)) / (2 - p))))
    elif (p == 0):
        dev = ((y_true - y_pred) ** 2)
    elif (p < 1):
        raise ValueError('Tweedie deviance is only defined for p<=0 and p>=1.')
    elif (p == 1):
        if ((y_true < 0).any() or (y_pred <= 0).any()):
            raise ValueError((message + 'non-negative y_true and strictly positive y_pred.'))
        dev = (2 * ((xlogy(y_true, (y_true / y_pred)) - y_true) + y_pred))
    elif (p == 2):
        if ((y_true <= 0).any() or (y_pred <= 0).any()):
            raise ValueError((message + 'strictly positive y_true and y_pred.'))
        dev = (2 * ((np.log((y_pred / y_true)) + (y_true / y_pred)) - 1))
    else:
        if (p < 2):
            if ((y_true < 0).any() or (y_pred <= 0).any()):
                raise ValueError((message + 'non-negative y_true and strictly positive y_pred.'))
        elif ((y_true <= 0).any() or (y_pred <= 0).any()):
            raise ValueError((message + 'strictly positive y_true and y_pred.'))
        dev = (2 * (((np.power(y_true, (2 - p)) / ((1 - p) * (2 - p))) - ((y_true * np.power(y_pred, (1 - p))) / (1 - p))) + (np.power(y_pred, (2 - p)) / (2 - p))))
    return np.average(dev, weights=sample_weight)