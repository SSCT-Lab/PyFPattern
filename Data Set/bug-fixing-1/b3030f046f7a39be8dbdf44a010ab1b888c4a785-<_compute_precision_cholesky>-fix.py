

def _compute_precision_cholesky(covariances, covariance_type):
    "Compute the Cholesky decomposition of the precisions.\n\n    Parameters\n    ----------\n    covariances : array-like\n        The covariance matrix of the current components.\n        The shape depends of the covariance_type.\n\n    covariance_type : {'full', 'tied', 'diag', 'spherical'}\n        The type of precision matrices.\n\n    Returns\n    -------\n    precisions_cholesky : array-like\n        The cholesky decomposition of sample precisions of the current\n        components. The shape depends of the covariance_type.\n    "
    estimate_precision_error_message = 'Fitting the mixture model failed because some components have ill-defined empirical covariance (for instance caused by singleton or collapsed samples). Try to decrease the number of components, or increase reg_covar.'
    if (covariance_type == 'full'):
        (n_components, n_features, _) = covariances.shape
        precisions_chol = np.empty((n_components, n_features, n_features))
        for (k, covariance) in enumerate(covariances):
            try:
                cov_chol = linalg.cholesky(covariance, lower=True)
            except linalg.LinAlgError:
                raise ValueError(estimate_precision_error_message)
            precisions_chol[k] = linalg.solve_triangular(cov_chol, np.eye(n_features), lower=True).T
    elif (covariance_type == 'tied'):
        (_, n_features) = covariances.shape
        try:
            cov_chol = linalg.cholesky(covariances, lower=True)
        except linalg.LinAlgError:
            raise ValueError(estimate_precision_error_message)
        precisions_chol = linalg.solve_triangular(cov_chol, np.eye(n_features), lower=True).T
    else:
        if np.any(np.less_equal(covariances, 0.0)):
            raise ValueError(estimate_precision_error_message)
        precisions_chol = (1.0 / np.sqrt(covariances))
    return precisions_chol
