def _check_accum_op(self, name, check_dtype=True):
    func = getattr(np, name)
    tm.assert_numpy_array_equal(func(self.ts).values, func(np.array(self.ts)), check_dtype=check_dtype)
    ts = self.ts.copy()
    ts[::2] = np.NaN
    result = func(ts)[1::2]
    expected = func(np.array(ts.dropna()))
    tm.assert_numpy_array_equal(result.values, expected, check_dtype=False)