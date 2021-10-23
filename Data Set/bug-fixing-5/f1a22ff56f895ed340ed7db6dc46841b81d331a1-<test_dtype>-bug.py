def test_dtype(self):
    assert (self.ts.dtype == np.dtype('float64'))
    assert (self.ts.dtypes == np.dtype('float64'))
    assert (self.ts.ftype == 'float64:dense')
    assert (self.ts.ftypes == 'float64:dense')
    tm.assert_series_equal(self.ts.get_dtype_counts(), Series(1, ['float64']))
    with tm.assert_produces_warning(FutureWarning):
        tm.assert_series_equal(self.ts.get_ftype_counts(), Series(1, ['float64:dense']))