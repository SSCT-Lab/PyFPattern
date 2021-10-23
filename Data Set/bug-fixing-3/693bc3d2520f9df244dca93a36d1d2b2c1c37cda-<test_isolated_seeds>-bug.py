def test_isolated_seeds():
    np.random.seed(0)
    a = np.random.random((7, 7))
    mask = (- np.ones(a.shape))
    mask[(1, 1)] = 1
    mask[3:, 3:] = 0
    mask[(4, 4)] = 2
    mask[(6, 6)] = 1
    res = random_walker(a, mask)
    assert (res[(1, 1)] == 1)
    res = random_walker(a, mask, return_full_prob=True)
    assert (res[(0, 1, 1)] == 1)
    assert (res[(1, 1, 1)] == 0)