

def f_regression(X, y, center=True):
    'Univariate linear regression tests.\n\n    Linear model for testing the individual effect of each of many regressors.\n    This is a scoring function to be used in a feature seletion procedure, not\n    a free standing feature selection procedure.\n\n    This is done in 2 steps:\n\n    1. The correlation between each regressor and the target is computed,\n       that is, ((X[:, i] - mean(X[:, i])) * (y - mean_y)) / (std(X[:, i]) *\n       std(y)).\n    2. It is converted to an F score then to a p-value.\n\n    For more on usage see the :ref:`User Guide <univariate_feature_selection>`.\n\n    Parameters\n    ----------\n    X : {array-like, sparse matrix}  shape = (n_samples, n_features)\n        The set of regressors that will be tested sequentially.\n\n    y : array of shape(n_samples).\n        The data matrix\n\n    center : True, bool,\n        If true, X and y will be centered.\n\n    Returns\n    -------\n    F : array, shape=(n_features,)\n        F values of features.\n\n    pval : array, shape=(n_features,)\n        p-values of F-scores.\n\n\n    See also\n    --------\n    mutual_info_regression: Mutual information for a continuous target.\n    f_classif: ANOVA F-value between label/feature for classification tasks.\n    chi2: Chi-squared stats of non-negative features for classification tasks.\n    SelectKBest: Select features based on the k highest scores.\n    SelectFpr: Select features based on a false positive rate test.\n    SelectFdr: Select features based on an estimated false discovery rate.\n    SelectFwe: Select features based on family-wise error rate.\n    SelectPercentile: Select features based on percentile of the highest\n        scores.\n    '
    (X, y) = check_X_y(X, y, ['csr', 'csc', 'coo'], dtype=np.float64)
    n_samples = X.shape[0]
    if center:
        y = (y - np.mean(y))
        if issparse(X):
            X_means = X.mean(axis=0).getA1()
        else:
            X_means = X.mean(axis=0)
        X_norms = np.sqrt((row_norms(X.T, squared=True) - (n_samples * (X_means ** 2))))
    else:
        X_norms = row_norms(X.T)
    corr = safe_sparse_dot(y, X)
    corr /= X_norms
    corr /= np.linalg.norm(y)
    degrees_of_freedom = (y.size - (2 if center else 1))
    F = (((corr ** 2) / (1 - (corr ** 2))) * degrees_of_freedom)
    pv = stats.f.sf(F, 1, degrees_of_freedom)
    return (F, pv)
