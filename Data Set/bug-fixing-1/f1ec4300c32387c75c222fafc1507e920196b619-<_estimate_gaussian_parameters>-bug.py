

def _estimate_gaussian_parameters(X, resp, reg_covar, covariance_type):
    "Estimate the Gaussian distribution parameters.\n\n    Parameters\n    ----------\n    X : array-like, shape (n_samples, n_features)\n        The input data array.\n\n    resp : array-like, shape (n_samples, n_features)\n        The responsibilities for each data sample in X.\n\n    reg_covar : float\n        The regularization added to the diagonal of the covariance matrices.\n\n    covariance_type : {'full', 'tied', 'diag', 'spherical'}\n        The type of precision matrices.\n\n    Returns\n    -------\n    nk : array-like, shape (n_components,)\n        The numbers of data samples in the current components.\n\n    means : array-like, shape (n_components, n_features)\n        The centers of the current components.\n\n    covariances : array-like\n        The covariance matrix of the current components.\n        The shape depends of the covariance_type.\n    "
    nk = (resp.sum(axis=0) + (10 * np.finfo(resp.dtype).eps))
    means = (np.dot(resp.T, X) / nk[:, np.newaxis])
    covariances = {
        'full': _estimate_gaussian_covariances_full,
        'tied': _estimate_gaussian_covariances_tied,
        'diag': _estimate_gaussian_covariances_diag,
        'spherical': _estimate_gaussian_covariances_spherical,
    }[covariance_type](resp, X, nk, means, reg_covar)
    return (nk, means, covariances)
