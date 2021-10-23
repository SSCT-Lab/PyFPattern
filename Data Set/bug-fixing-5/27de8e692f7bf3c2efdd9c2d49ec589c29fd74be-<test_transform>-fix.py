def test_transform(self, string_series):
    with np.errstate(all='ignore'):
        f_sqrt = np.sqrt(string_series)
        f_abs = np.abs(string_series)
        result = string_series.transform(np.sqrt)
        expected = f_sqrt.copy()
        assert_series_equal(result, expected)
        result = string_series.apply(np.sqrt)
        assert_series_equal(result, expected)
        result = string_series.transform([np.sqrt])
        expected = f_sqrt.to_frame().copy()
        expected.columns = ['sqrt']
        assert_frame_equal(result, expected)
        result = string_series.transform([np.sqrt])
        assert_frame_equal(result, expected)
        result = string_series.transform(['sqrt'])
        assert_frame_equal(result, expected)
        expected = pd.concat([f_sqrt, f_abs], axis=1)
        expected.columns = ['sqrt', 'absolute']
        result = string_series.apply([np.sqrt, np.abs])
        assert_frame_equal(result, expected)
        result = string_series.transform(['sqrt', 'abs'])
        expected.columns = ['sqrt', 'abs']
        assert_frame_equal(result, expected)
        expected = pd.concat([f_sqrt, f_abs], axis=1)
        expected.columns = ['foo', 'bar']
        expected = expected.unstack().rename('series')
        result = string_series.apply({
            'foo': np.sqrt,
            'bar': np.abs,
        })
        assert_series_equal(result.reindex_like(expected), expected)