def test_tmax(self):
    assert_equal(stats.tmax(4), 4)
    x = np.arange(10)
    assert_equal(stats.tmax(x), 9)
    assert_equal(stats.tmax(x, upperlimit=9), 9)
    assert_equal(stats.tmax(x, upperlimit=9, inclusive=False), 8)
    x = x.reshape((5, 2))
    assert_equal(stats.tmax(x, upperlimit=9, inclusive=False), [8, 7])
    assert_equal(stats.tmax(x, axis=1), [1, 3, 5, 7, 9])
    assert_equal(stats.tmax(x, axis=None), 9)
    x = np.arange(10.0)
    x[6] = np.nan
    with suppress_warnings() as sup:
        r = sup.record(RuntimeWarning, 'invalid value*')
        assert_equal(stats.tmax(x), np.nan)
        assert_equal(stats.tmax(x, nan_policy='omit'), 9.0)
        assert_raises(ValueError, stats.tmax, x, nan_policy='raise')
        assert_raises(ValueError, stats.tmax, x, nan_policy='foobar')