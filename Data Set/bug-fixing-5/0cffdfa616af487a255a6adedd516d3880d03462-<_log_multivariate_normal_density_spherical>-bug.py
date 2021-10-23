def _log_multivariate_normal_density_spherical(X, means, covars):
    'Compute Gaussian log-density at X for a spherical model.'
    cv = covars.copy()
    if (covars.ndim == 1):
        cv = cv[:, np.newaxis]
    if (covars.shape[1] == 1):
        cv = np.tile(cv, (1, X.shape[(- 1)]))
    return _log_multivariate_normal_density_diag(X, means, cv)