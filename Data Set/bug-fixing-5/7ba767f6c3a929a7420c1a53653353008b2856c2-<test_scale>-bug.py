def test_scale(self):
    numpy_version = NumpyVersion(np.__version__)
    x = np.arange(15.0).reshape((3, 5))
    assert_equal(stats.iqr(x, scale='raw'), 7)
    assert_almost_equal(stats.iqr(x, scale='normal'), (7 / 1.3489795))
    assert_equal(stats.iqr(x, scale=2.0), 3.5)
    x[(1, 2)] = np.nan
    if (numpy_version < '1.10.0a'):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            assert_equal(stats.iqr(x, scale='raw', nan_policy='propagate'), 8)
            assert_almost_equal(stats.iqr(x, scale='normal', nan_policy='propagate'), (8 / 1.3489795))
            assert_equal(stats.iqr(x, scale=2.0, nan_policy='propagate'), 4)
            if (numpy_version < '1.9.0a'):
                assert_equal(stats.iqr(x, axis=1, nan_policy='propagate'), [2, 3, 2])
                assert_almost_equal(stats.iqr(x, axis=1, scale='normal', nan_policy='propagate'), (np.array([2, 3, 2]) / 1.3489795))
                assert_equal(stats.iqr(x, axis=1, scale=2.0, nan_policy='propagate'), [1, 1.5, 1])
            else:
                assert_equal(stats.iqr(x, axis=1, nan_policy='propagate'), [2, np.nan, 2])
                assert_almost_equal(stats.iqr(x, axis=1, scale='normal', nan_policy='propagate'), (np.array([2, np.nan, 2]) / 1.3489795))
                assert_equal(stats.iqr(x, axis=1, scale=2.0, nan_policy='propagate'), [1, np.nan, 1])
            _check_warnings(w, RuntimeWarning, 6)
    else:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            assert_equal(stats.iqr(x, scale='raw', nan_policy='propagate'), np.nan)
            assert_equal(stats.iqr(x, scale='normal', nan_policy='propagate'), np.nan)
            assert_equal(stats.iqr(x, scale=2.0, nan_policy='propagate'), np.nan)
            assert_equal(stats.iqr(x, axis=1, scale='raw', nan_policy='propagate'), [2, np.nan, 2])
            assert_almost_equal(stats.iqr(x, axis=1, scale='normal', nan_policy='propagate'), (np.array([2, np.nan, 2]) / 1.3489795))
            assert_equal(stats.iqr(x, axis=1, scale=2.0, nan_policy='propagate'), [1, np.nan, 1])
            _check_warnings(w, RuntimeWarning, 6)
    if (numpy_version < '1.9.0a'):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            assert_equal(stats.iqr(x, scale='raw', nan_policy='omit'), 8)
            assert_almost_equal(stats.iqr(x, scale='normal', nan_policy='omit'), (8 / 1.3489795))
            assert_equal(stats.iqr(x, scale=2.0, nan_policy='omit'), 4)
            _check_warnings(w, RuntimeWarning, 3)
    else:
        assert_equal(stats.iqr(x, scale='raw', nan_policy='omit'), 7.5)
        assert_almost_equal(stats.iqr(x, scale='normal', nan_policy='omit'), (7.5 / 1.3489795))
        assert_equal(stats.iqr(x, scale=2.0, nan_policy='omit'), 3.75)
    assert_raises(ValueError, stats.iqr, x, scale='foobar')