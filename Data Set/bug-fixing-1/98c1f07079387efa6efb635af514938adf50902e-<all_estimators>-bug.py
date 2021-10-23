

def all_estimators(include_meta_estimators=None, include_other=None, type_filter=None, include_dont_test=None):
    "Get a list of all estimators from sklearn.\n\n    This function crawls the module and gets all classes that inherit\n    from BaseEstimator. Classes that are defined in test-modules are not\n    included.\n    By default meta_estimators such as GridSearchCV are also not included.\n\n    Parameters\n    ----------\n    include_meta_estimators : boolean, default=False\n        Deprecated, ignored.\n        .. deprecated:: 0.21\n           ``include_meta_estimators`` has been deprecated and has no effect in\n           0.21 and will be removed in 0.23.\n\n    include_other : boolean, default=False\n        Deprecated, ignored.\n        .. deprecated:: 0.21\n           ``include_other`` has been deprecated and has not effect in 0.21 and\n           will be removed in 0.23.\n\n    type_filter : string, list of string,  or None, default=None\n        Which kind of estimators should be returned. If None, no filter is\n        applied and all estimators are returned.  Possible values are\n        'classifier', 'regressor', 'cluster' and 'transformer' to get\n        estimators only of these specific types, or a list of these to\n        get the estimators that fit at least one of the types.\n\n    include_dont_test : boolean, default=False\n        Deprecated, ignored.\n        .. deprecated:: 0.21\n           ``include_dont_test`` has been deprecated and has no effect in 0.21\n           and will be removed in 0.23.\n\n    Returns\n    -------\n    estimators : list of tuples\n        List of (name, class), where ``name`` is the class name as string\n        and ``class`` is the actuall type of the class.\n    "

    def is_abstract(c):
        if (not hasattr(c, '__abstractmethods__')):
            return False
        if (not len(c.__abstractmethods__)):
            return False
        return True
    if (include_other is not None):
        warnings.warn('include_other was deprecated in version 0.21, has no effect and will be removed in 0.23', DeprecationWarning)
    if (include_dont_test is not None):
        warnings.warn('include_dont_test was deprecated in version 0.21, has no effect and will be removed in 0.23', DeprecationWarning)
    if (include_meta_estimators is not None):
        warnings.warn('include_meta_estimators was deprecated in version 0.21, has no effect and will be removed in 0.23', DeprecationWarning)
    all_classes = []
    path = sklearn.__path__
    for (importer, modname, ispkg) in pkgutil.walk_packages(path=path, prefix='sklearn.', onerror=(lambda x: None)):
        if ('.tests.' in modname):
            continue
        if (IS_PYPY and (('_svmlight_format' in modname) or ('feature_extraction._hashing' in modname))):
            continue
        module = __import__(modname, fromlist='dummy')
        classes = inspect.getmembers(module, inspect.isclass)
        all_classes.extend(classes)
    all_classes = set(all_classes)
    estimators = [c for c in all_classes if (issubclass(c[1], BaseEstimator) and (c[0] != 'BaseEstimator'))]
    estimators = [c for c in estimators if (not is_abstract(c[1]))]
    if (type_filter is not None):
        if (not isinstance(type_filter, list)):
            type_filter = [type_filter]
        else:
            type_filter = list(type_filter)
        filtered_estimators = []
        filters = {
            'classifier': ClassifierMixin,
            'regressor': RegressorMixin,
            'transformer': TransformerMixin,
            'cluster': ClusterMixin,
        }
        for (name, mixin) in filters.items():
            if (name in type_filter):
                type_filter.remove(name)
                filtered_estimators.extend([est for est in estimators if issubclass(est[1], mixin)])
        estimators = filtered_estimators
        if type_filter:
            raise ValueError(("Parameter type_filter must be 'classifier', 'regressor', 'transformer', 'cluster' or None, got %s." % repr(type_filter)))
    return sorted(set(estimators), key=itemgetter(0))
