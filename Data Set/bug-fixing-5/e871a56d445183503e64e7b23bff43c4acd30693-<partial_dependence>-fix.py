@deprecated('The function ensemble.partial_dependence has been deprecated in favour of inspection.partial_dependence in 0.21 and will be removed in 0.23.')
def partial_dependence(gbrt, target_variables, grid=None, X=None, percentiles=(0.05, 0.95), grid_resolution=100):
    'Partial dependence of ``target_variables``.\n\n    Partial dependence plots show the dependence between the joint values\n    of the ``target_variables`` and the function represented\n    by the ``gbrt``.\n\n    Read more in the :ref:`User Guide <partial_dependence>`.\n\n    .. deprecated:: 0.21\n       This function was deprecated in version 0.21 in favor of\n       :func:`sklearn.inspection.partial_dependence` and will be\n       removed in 0.23.\n\n    Parameters\n    ----------\n    gbrt : BaseGradientBoosting\n        A fitted gradient boosting model.\n    target_variables : array-like, dtype=int\n        The target features for which the partial dependency should be\n        computed (size should be smaller than 3 for visual renderings).\n    grid : array-like, shape=(n_points, len(target_variables))\n        The grid of ``target_variables`` values for which the\n        partial dependency should be evaluated (either ``grid`` or ``X``\n        must be specified).\n    X : array-like, shape=(n_samples, n_features)\n        The data on which ``gbrt`` was trained. It is used to generate\n        a ``grid`` for the ``target_variables``. The ``grid`` comprises\n        ``grid_resolution`` equally spaced points between the two\n        ``percentiles``.\n    percentiles : (low, high), default=(0.05, 0.95)\n        The lower and upper percentile used create the extreme values\n        for the ``grid``. Only if ``X`` is not None.\n    grid_resolution : int, default=100\n        The number of equally spaced points on the ``grid``.\n\n    Returns\n    -------\n    pdp : array, shape=(n_classes, n_points)\n        The partial dependence function evaluated on the ``grid``.\n        For regression and binary classification ``n_classes==1``.\n    axes : seq of ndarray or None\n        The axes with which the grid has been created or None if\n        the grid has been given.\n\n    Examples\n    --------\n    >>> samples = [[0, 0, 2], [1, 0, 0]]\n    >>> labels = [0, 1]\n    >>> from sklearn.ensemble import GradientBoostingClassifier\n    >>> gb = GradientBoostingClassifier(random_state=0).fit(samples, labels)\n    >>> kwargs = dict(X=samples, percentiles=(0, 1), grid_resolution=2)\n    >>> partial_dependence(gb, [0], **kwargs) # doctest: +SKIP\n    (array([[-4.52...,  4.52...]]), [array([ 0.,  1.])])\n    '
    if (not isinstance(gbrt, BaseGradientBoosting)):
        raise ValueError('gbrt has to be an instance of BaseGradientBoosting')
    check_is_fitted(gbrt, 'estimators_')
    if (((grid is None) and (X is None)) or ((grid is not None) and (X is not None))):
        raise ValueError('Either grid or X must be specified')
    target_variables = np.asarray(target_variables, dtype=np.int32, order='C').ravel()
    if any([(not (0 <= fx < gbrt.n_features_)) for fx in target_variables]):
        raise ValueError(('target_variables must be in [0, %d]' % (gbrt.n_features_ - 1)))
    if (X is not None):
        X = check_array(X, dtype=DTYPE, order='C')
        (grid, axes) = _grid_from_X(X[:, target_variables], percentiles, grid_resolution)
    else:
        assert (grid is not None)
        axes = None
        if (grid.ndim == 1):
            grid = grid[:, np.newaxis]
        if (grid.ndim != 2):
            raise ValueError(('grid must be 2d but is %dd' % grid.ndim))
    grid = np.asarray(grid, dtype=DTYPE, order='C')
    assert (grid.shape[1] == target_variables.shape[0])
    n_trees_per_stage = gbrt.estimators_.shape[1]
    n_estimators = gbrt.estimators_.shape[0]
    pdp = np.zeros((n_trees_per_stage, grid.shape[0]), dtype=np.float64, order='C')
    for stage in range(n_estimators):
        for k in range(n_trees_per_stage):
            tree = gbrt.estimators_[(stage, k)].tree_
            tree.compute_partial_dependence(grid, target_variables, pdp[k])
    pdp *= gbrt.learning_rate
    return (pdp, axes)