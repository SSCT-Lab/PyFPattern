def random_binomial(shape, p=0.0, dtype=_FLOATX, seed=None):
    if (seed is None):
        seed = np.random.randint(10000000.0)
    rng = RandomStreams(seed=seed)
    return rng.binomial(shape, p=p, dtype=dtype)