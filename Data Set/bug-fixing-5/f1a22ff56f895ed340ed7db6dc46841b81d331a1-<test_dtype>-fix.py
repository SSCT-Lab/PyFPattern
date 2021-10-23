def test_dtype(self, datetime_series):
    assert (datetime_series.dtype == np.dtype('float64'))
    assert (datetime_series.dtypes == np.dtype('float64'))
    assert (datetime_series.ftype == 'float64:dense')
    assert (datetime_series.ftypes == 'float64:dense')
    tm.assert_series_equal(datetime_series.get_dtype_counts(), Series(1, ['float64']))
    with tm.assert_produces_warning(FutureWarning):
        tm.assert_series_equal(datetime_series.get_ftype_counts(), Series(1, ['float64:dense']))