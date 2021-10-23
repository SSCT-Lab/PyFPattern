def _lnB(alpha):
    '\n    Internal helper function to compute the log of the useful quotient\n\n    .. math::\n\n        B(\\alpha) = \\frac{\\prod_{i=1}{K}\\Gamma(\\alpha_i)}\n                         {\\Gamma\\left(\\sum_{i=1}^{K} \\alpha_i \\right)}\n\n    Parameters\n    ----------\n    %(_dirichlet_doc_default_callparams)s\n\n    Returns\n    -------\n    B : scalar\n        Helper quotient, internal use only\n\n    '
    return (np.sum(gammaln(alpha)) - gammaln(np.sum(alpha)))