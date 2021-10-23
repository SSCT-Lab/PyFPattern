@td.skip_if_no_scipy
def test_corr(self):
    import scipy.stats as stats
    tm.assert_almost_equal(self.ts.corr(self.ts), 1)
    tm.assert_almost_equal(self.ts[:15].corr(self.ts[5:]), 1)
    assert isna(self.ts[:15].corr(self.ts[5:], min_periods=12))
    ts1 = self.ts[:15].reindex(self.ts.index)
    ts2 = self.ts[5:].reindex(self.ts.index)
    assert isna(ts1.corr(ts2, min_periods=12))
    assert np.isnan(self.ts[::2].corr(self.ts[1::2]))
    cp = self.ts[:10].copy()
    cp[:] = np.nan
    assert isna(cp.corr(cp))
    A = tm.makeTimeSeries()
    B = tm.makeTimeSeries()
    result = A.corr(B)
    (expected, _) = stats.pearsonr(A, B)
    tm.assert_almost_equal(result, expected)