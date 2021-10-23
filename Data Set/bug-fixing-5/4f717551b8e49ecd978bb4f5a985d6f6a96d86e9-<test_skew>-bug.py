@td.skip_if_no_scipy
def test_skew(self):
    from scipy.stats import skew
    alt = (lambda x: skew(x, bias=False))
    self._check_stat_op('skew', alt)
    min_N = 3
    for i in range(1, (min_N + 1)):
        s = Series(np.ones(i))
        df = DataFrame(np.ones((i, i)))
        if (i < min_N):
            assert np.isnan(s.skew())
            assert np.isnan(df.skew()).all()
        else:
            assert (0 == s.skew())
            assert (df.skew() == 0).all()