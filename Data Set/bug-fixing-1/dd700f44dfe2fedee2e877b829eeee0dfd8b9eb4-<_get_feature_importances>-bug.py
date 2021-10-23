

def _get_feature_importances(estimator, norm_order=1):
    'Retrieve or aggregate feature importances from estimator'
    importances = getattr(estimator, 'feature_importances_', None)
    if ((importances is None) and hasattr(estimator, 'coef_')):
        if (estimator.coef_.ndim == 1):
            importances = np.abs(estimator.coef_)
        else:
            importances = np.linalg.norm(estimator.coef_, axis=0, ord=norm_order)
    elif (importances is None):
        raise ValueError(('The underlying estimator %s has no `coef_` or `feature_importances_` attribute. Either pass a fitted estimator to SelectFromModel or call fit before calling transform.' % estimator.__class__.__name__))
    return importances
