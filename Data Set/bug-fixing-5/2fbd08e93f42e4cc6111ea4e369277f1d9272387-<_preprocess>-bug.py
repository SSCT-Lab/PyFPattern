def _preprocess(self, x, skew):
    loc = 0.0
    scale = 1.0
    norm2pearson_transition = 1.6e-05
    (ans, x, skew) = np.broadcast_arrays([1.0], x, skew)
    ans = ans.copy()
    mask = (np.absolute(skew) < norm2pearson_transition)
    invmask = (~ mask)
    beta = (2.0 / (skew[invmask] * scale))
    alpha = ((scale * beta) ** 2)
    zeta = (loc - (alpha / beta))
    transx = (beta * (x[invmask] - zeta))
    return (ans, x, transx, skew, mask, invmask, beta, alpha, zeta)