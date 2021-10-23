def dirichlet_expectation(alpha):
    'For a vector :math:`\\theta \\sim Dir(\\alpha)`, compute :math:`E[log \\theta]`.\n\n    Parameters\n    ----------\n    alpha : numpy.ndarray\n        Input vector or matrix.\n\n    Returns\n    -------\n    numpy.ndarray:\n        :math:`E[log \\theta]`\n\n    '
    if (len(alpha.shape) == 1):
        result = (psi(alpha) - psi(np.sum(alpha)))
    else:
        result = (psi(alpha) - psi(np.sum(alpha, 1))[:, np.newaxis])
    return result.astype(alpha.dtype, copy=False)