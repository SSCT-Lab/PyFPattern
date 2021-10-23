

def assoc_laguerre(x, n, k=0.0):
    'Compute nth-order generalized (associated) Laguerre polynomial.\n\n    The polynomial :math:`L^(alpha)_n(x)` is orthogonal over ``[0, inf)``,\n    with weighting function ``exp(-x) * x**alpha`` with ``alpha > -1``.\n\n    Notes\n    -----\n    `assoc_laguerre` is a simple wrapper around `eval_genlaguerre`, with\n    reversed argument order ``(x, n, k=0.0) --> (n, k, x)``.\n\n    '
    return orthogonal.eval_genlaguerre(n, k, x)
