def dropout(x, level, seed=None):
    if ((level < 0.0) or (level >= 1)):
        raise Exception('Dropout level must be in interval [0, 1[.')
    if (seed is None):
        seed = np.random.randint(10000000.0)
    rng = RandomStreams(seed=seed)
    retain_prob = (1.0 - level)
    x *= rng.binomial(x.shape, p=retain_prob, dtype=x.dtype)
    x /= retain_prob
    return x