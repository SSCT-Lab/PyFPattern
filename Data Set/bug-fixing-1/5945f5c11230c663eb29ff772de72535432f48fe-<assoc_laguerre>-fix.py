

def assoc_laguerre(x, n, k=0.0):
    'Compute the generalized (associated) Laguerre polynomial of degree n and order k.\n\n    The polynomial :math:`L^{(k)}_n(x)` is orthogonal over ``[0, inf)``,\n    with weighting function ``exp(-x) * x**k`` with ``k > -1``.\n\n    Notes\n    -----\n    `assoc_laguerre` is a simple wrapper around `eval_genlaguerre`, with\n    reversed argument order ``(x, n, k=0.0) --> (n, k, x)``.\n\n    '
    return orthogonal.eval_genlaguerre(n, k, x)
