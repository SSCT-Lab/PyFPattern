def random_normal(shape, mean=0.0, std=1.0, dtype=_FLOATX, seed=None):
    if (seed is None):
        seed = np.random.randint(1, 10000000.0)
    rng = RandomStreams(seed=seed)
    return rng.normal(size=shape, avg=mean, std=std, dtype=dtype)