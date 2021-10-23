def test_with_nested_series(self):
    result = self.ts.apply((lambda x: Series([x, (x ** 2)], index=['x', 'x^2'])))
    expected = DataFrame({
        'x': self.ts,
        'x^2': (self.ts ** 2),
    })
    tm.assert_frame_equal(result, expected)
    result = self.ts.agg((lambda x: Series([x, (x ** 2)], index=['x', 'x^2'])))
    tm.assert_frame_equal(result, expected)