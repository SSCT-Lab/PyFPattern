def test_with_nested_series(self, datetime_series):
    result = datetime_series.apply((lambda x: Series([x, (x ** 2)], index=['x', 'x^2'])))
    expected = DataFrame({
        'x': datetime_series,
        'x^2': (datetime_series ** 2),
    })
    tm.assert_frame_equal(result, expected)
    result = datetime_series.agg((lambda x: Series([x, (x ** 2)], index=['x', 'x^2'])))
    tm.assert_frame_equal(result, expected)