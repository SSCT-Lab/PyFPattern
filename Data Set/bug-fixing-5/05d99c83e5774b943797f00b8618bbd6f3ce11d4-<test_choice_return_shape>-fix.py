def test_choice_return_shape(self):
    p = [0.1, 0.9]
    assert_(np.isscalar(np.random.choice(2, replace=True)))
    assert_(np.isscalar(np.random.choice(2, replace=False)))
    assert_(np.isscalar(np.random.choice(2, replace=True, p=p)))
    assert_(np.isscalar(np.random.choice(2, replace=False, p=p)))
    assert_(np.isscalar(np.random.choice([1, 2], replace=True)))
    assert_((np.random.choice([None], replace=True) is None))
    a = np.array([1, 2])
    arr = np.empty(1, dtype=object)
    arr[0] = a
    assert_((np.random.choice(arr, replace=True) is a))
    s = tuple()
    assert_((not np.isscalar(np.random.choice(2, s, replace=True))))
    assert_((not np.isscalar(np.random.choice(2, s, replace=False))))
    assert_((not np.isscalar(np.random.choice(2, s, replace=True, p=p))))
    assert_((not np.isscalar(np.random.choice(2, s, replace=False, p=p))))
    assert_((not np.isscalar(np.random.choice([1, 2], s, replace=True))))
    assert_((np.random.choice([None], s, replace=True).ndim == 0))
    a = np.array([1, 2])
    arr = np.empty(1, dtype=object)
    arr[0] = a
    assert_((np.random.choice(arr, s, replace=True).item() is a))
    s = (2, 3)
    p = [0.1, 0.1, 0.1, 0.1, 0.4, 0.2]
    assert_equal(np.random.choice(6, s, replace=True).shape, s)
    assert_equal(np.random.choice(6, s, replace=False).shape, s)
    assert_equal(np.random.choice(6, s, replace=True, p=p).shape, s)
    assert_equal(np.random.choice(6, s, replace=False, p=p).shape, s)
    assert_equal(np.random.choice(np.arange(6), s, replace=True).shape, s)