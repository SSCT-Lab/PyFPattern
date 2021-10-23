def test_transform_and_agg_error(self, string_series):

    def f():
        string_series.transform(['min', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            string_series.agg(['sqrt', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            string_series.transform(['sqrt', 'max'])
    pytest.raises(ValueError, f)

    def f():
        with np.errstate(all='ignore'):
            string_series.agg({
                'foo': np.sqrt,
                'bar': 'sum',
            })
    pytest.raises(ValueError, f)