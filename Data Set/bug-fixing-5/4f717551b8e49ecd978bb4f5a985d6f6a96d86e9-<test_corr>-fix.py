@td.skip_if_no_scipy
def test_corr(self, datetime_series):
    import scipy.stats as stats
    tm.assert_almost_equal(datetime_series.corr(datetime_series), 1)
    tm.assert_almost_equal(datetime_series[:15].corr(datetime_series[5:]), 1)
    assert isna(datetime_series[:15].corr(datetime_series[5:], min_periods=12))
    ts1 = datetime_series[:15].reindex(datetime_series.index)
    ts2 = datetime_series[5:].reindex(datetime_series.index)
    assert isna(ts1.corr(ts2, min_periods=12))
    assert np.isnan(datetime_series[::2].corr(datetime_series[1::2]))
    cp = datetime_series[:10].copy()
    cp[:] = np.nan
    assert isna(cp.corr(cp))
    A = tm.makeTimeSeries()
    B = tm.makeTimeSeries()
    result = A.corr(B)
    (expected, _) = stats.pearsonr(A, B)
    tm.assert_almost_equal(result, expected)