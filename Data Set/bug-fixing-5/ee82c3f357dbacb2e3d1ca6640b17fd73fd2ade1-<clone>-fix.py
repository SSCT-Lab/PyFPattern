def clone(estimator, safe=True):
    'Constructs a new estimator with the same parameters.\n\n    Clone does a deep copy of the model in an estimator\n    without actually copying attached data. It yields a new estimator\n    with the same parameters that has not been fit on any data.\n\n    Parameters\n    ----------\n    estimator : estimator object, or list, tuple or set of objects\n        The estimator or group of estimators to be cloned\n\n    safe : boolean, optional\n        If safe is false, clone will fall back to a deep copy on objects\n        that are not estimators.\n\n    '
    estimator_type = type(estimator)
    if (estimator_type in (list, tuple, set, frozenset)):
        return estimator_type([clone(e, safe=safe) for e in estimator])
    elif (not hasattr(estimator, 'get_params')):
        if (not safe):
            return copy.deepcopy(estimator)
        else:
            raise TypeError(("Cannot clone object '%s' (type %s): it does not seem to be a scikit-learn estimator as it does not implement a 'get_params' methods." % (repr(estimator), type(estimator))))
    klass = estimator.__class__
    new_object_params = estimator.get_params(deep=False)
    for (name, param) in six.iteritems(new_object_params):
        new_object_params[name] = clone(param, safe=False)
    new_object = klass(**new_object_params)
    params_set = new_object.get_params(deep=False)
    for name in new_object_params:
        param1 = new_object_params[name]
        param2 = params_set[name]
        if (param1 is param2):
            continue
        if isinstance(param1, np.ndarray):
            if (not isinstance(param2, type(param1))):
                equality_test = False
            elif ((param1.ndim > 0) and (param1.shape[0] > 0) and isinstance(param2, np.ndarray) and (param2.ndim > 0) and (param2.shape[0] > 0)):
                equality_test = ((param1.shape == param2.shape) and (param1.dtype == param2.dtype) and (_first_and_last_element(param1) == _first_and_last_element(param2)))
            else:
                equality_test = np.all((param1 == param2))
        elif sparse.issparse(param1):
            if (not sparse.issparse(param2)):
                equality_test = False
            elif ((param1.size == 0) or (param2.size == 0)):
                equality_test = ((param1.__class__ == param2.__class__) and (param1.size == 0) and (param2.size == 0))
            else:
                equality_test = ((param1.__class__ == param2.__class__) and (_first_and_last_element(param1) == _first_and_last_element(param2)) and (param1.nnz == param2.nnz) and (param1.shape == param2.shape))
        else:
            equality_test = (param1 == param2)
        if equality_test:
            warnings.warn(('Estimator %s modifies parameters in __init__. This behavior is deprecated as of 0.18 and support for this behavior will be removed in 0.20.' % type(estimator).__name__), DeprecationWarning)
        else:
            raise RuntimeError(('Cannot clone object %s, as the constructor does not seem to set parameter %s' % (estimator, name)))
    return new_object