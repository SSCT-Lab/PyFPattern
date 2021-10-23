def _check_accum_op(self, name, datetime_series_, check_dtype=True):
    func = getattr(np, name)
    tm.assert_numpy_array_equal(func(datetime_series_).values, func(np.array(datetime_series_)), check_dtype=check_dtype)
    ts = datetime_series_.copy()
    ts[::2] = np.NaN
    result = func(ts)[1::2]
    expected = func(np.array(ts.dropna()))
    tm.assert_numpy_array_equal(result.values, expected, check_dtype=False)