def dirichlet_expectation(alpha):
    '\n    For a vector `theta~Dir(alpha)`, compute `E[log(theta)]`.\n    '
    if (len(alpha.shape) == 1):
        result = (psi(alpha) - psi(np.sum(alpha)))
    else:
        result = (psi(alpha) - psi(np.sum(alpha, 1))[:, np.newaxis])
    return result.astype(alpha.dtype, copy=False)