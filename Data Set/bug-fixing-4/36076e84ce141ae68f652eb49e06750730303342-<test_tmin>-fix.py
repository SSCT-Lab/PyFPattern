def test_tmin(self):
    assert_equal(stats.tmin(4), 4)
    x = np.arange(10)
    assert_equal(stats.tmin(x), 0)
    assert_equal(stats.tmin(x, lowerlimit=0), 0)
    assert_equal(stats.tmin(x, lowerlimit=0, inclusive=False), 1)
    x = x.reshape((5, 2))
    assert_equal(stats.tmin(x, lowerlimit=0, inclusive=False), [2, 1])
    assert_equal(stats.tmin(x, axis=1), [0, 2, 4, 6, 8])
    assert_equal(stats.tmin(x, axis=None), 0)
    x = np.arange(10.0)
    x[9] = np.nan
    with suppress_warnings() as sup:
        r = sup.record(RuntimeWarning, 'invalid value*')
        assert_equal(stats.tmin(x), np.nan)
        assert_equal(stats.tmin(x, nan_policy='omit'), 0.0)
        assert_raises(ValueError, stats.tmin, x, nan_policy='raise')
        assert_raises(ValueError, stats.tmin, x, nan_policy='foobar')
        assert_raises_regex(ValueError, "'propagate', 'raise', 'omit'", stats.tmin, x, nan_policy='foo')