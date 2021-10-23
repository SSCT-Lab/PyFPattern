def test_with_string_args(self, datetime_series):
    for arg in ['sum', 'mean', 'min', 'max', 'std']:
        result = datetime_series.apply(arg)
        expected = getattr(datetime_series, arg)()
        assert (result == expected)