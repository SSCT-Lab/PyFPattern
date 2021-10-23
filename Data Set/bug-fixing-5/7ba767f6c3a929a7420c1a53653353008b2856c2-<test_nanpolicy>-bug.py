def test_nanpolicy(self):
    numpy_version = NumpyVersion(np.__version__)
    x = np.arange(15.0).reshape((3, 5))
    assert_equal(stats.iqr(x, nan_policy='propagate'), 7)
    assert_equal(stats.iqr(x, nan_policy='omit'), 7)
    assert_equal(stats.iqr(x, nan_policy='raise'), 7)
    x[(1, 2)] = np.nan
    if (numpy_version < '1.10.0a'):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            assert_equal(stats.iqr(x, nan_policy='propagate'), 8)
            assert_equal(stats.iqr(x, axis=0, nan_policy='propagate'), [5, 5, np.nan, 5, 5])
            if (numpy_version < '1.9.0a'):
                assert_equal(stats.iqr(x, axis=1, nan_policy='propagate'), [2, 3, 2])
            else:
                assert_equal(stats.iqr(x, axis=1, nan_policy='propagate'), [2, np.nan, 2])
            _check_warnings(w, RuntimeWarning, 3)
    else:
        assert_equal(stats.iqr(x, nan_policy='propagate'), np.nan)
        assert_equal(stats.iqr(x, axis=0, nan_policy='propagate'), [5, 5, np.nan, 5, 5])
        assert_equal(stats.iqr(x, axis=1, nan_policy='propagate'), [2, np.nan, 2])
    if (numpy_version < '1.9.0a'):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            assert_equal(stats.iqr(x, nan_policy='omit'), 8)
            assert_equal(stats.iqr(x, axis=0, nan_policy='omit'), [5, 5, np.nan, 5, 5])
            assert_equal(stats.iqr(x, axis=1, nan_policy='omit'), [2, 3, 2])
            _check_warnings(w, RuntimeWarning, 3)
    else:
        assert_equal(stats.iqr(x, nan_policy='omit'), 7.5)
        assert_equal(stats.iqr(x, axis=0, nan_policy='omit'), (5 * np.ones(5)))
        assert_equal(stats.iqr(x, axis=1, nan_policy='omit'), [2, 2.5, 2])
    assert_raises(ValueError, stats.iqr, x, nan_policy='raise')
    assert_raises(ValueError, stats.iqr, x, axis=0, nan_policy='raise')
    assert_raises(ValueError, stats.iqr, x, axis=1, nan_policy='raise')
    assert_raises(ValueError, stats.iqr, x, nan_policy='barfood')