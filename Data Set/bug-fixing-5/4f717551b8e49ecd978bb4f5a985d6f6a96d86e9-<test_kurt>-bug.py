@td.skip_if_no_scipy
def test_kurt(self):
    from scipy.stats import kurtosis
    alt = (lambda x: kurtosis(x, bias=False))
    self._check_stat_op('kurt', alt)
    index = MultiIndex(levels=[['bar'], ['one', 'two', 'three'], [0, 1]], labels=[[0, 0, 0, 0, 0, 0], [0, 1, 2, 0, 1, 2], [0, 1, 0, 1, 0, 1]])
    s = Series(np.random.randn(6), index=index)
    tm.assert_almost_equal(s.kurt(), s.kurt(level=0)['bar'])
    min_N = 4
    for i in range(1, (min_N + 1)):
        s = Series(np.ones(i))
        df = DataFrame(np.ones((i, i)))
        if (i < min_N):
            assert np.isnan(s.kurt())
            assert np.isnan(df.kurt()).all()
        else:
            assert (0 == s.kurt())
            assert (df.kurt() == 0).all()