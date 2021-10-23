def test_cov(self):
    tm.assert_almost_equal(self.ts.cov(self.ts), (self.ts.std() ** 2))
    tm.assert_almost_equal(self.ts[:15].cov(self.ts[5:]), (self.ts[5:15].std() ** 2))
    assert np.isnan(self.ts[::2].cov(self.ts[1::2]))
    cp = self.ts[:10].copy()
    cp[:] = np.nan
    assert isna(cp.cov(cp))
    assert isna(self.ts[:15].cov(self.ts[5:], min_periods=12))
    ts1 = self.ts[:15].reindex(self.ts.index)
    ts2 = self.ts[5:].reindex(self.ts.index)
    assert isna(ts1.cov(ts2, min_periods=12))