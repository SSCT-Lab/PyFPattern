def random_uniform(shape, low=0.0, high=1.0, dtype=_FLOATX, seed=None):
    if (seed is None):
        seed = np.random.randint(10000000.0)
    rng = RandomStreams(seed=seed)
    return rng.uniform(shape, low=low, high=high, dtype=dtype)