def test_transform(self):
    with np.errstate(all='ignore'):
        f_sqrt = np.sqrt(self.series)
        f_abs = np.abs(self.series)
        result = self.series.transform(np.sqrt)
        expected = f_sqrt.copy()
        assert_series_equal(result, expected)
        result = self.series.apply(np.sqrt)
        assert_series_equal(result, expected)
        result = self.series.transform([np.sqrt])
        expected = f_sqrt.to_frame().copy()
        expected.columns = ['sqrt']
        assert_frame_equal(result, expected)
        result = self.series.transform([np.sqrt])
        assert_frame_equal(result, expected)
        result = self.series.transform(['sqrt'])
        assert_frame_equal(result, expected)
        expected = pd.concat([f_sqrt, f_abs], axis=1)
        expected.columns = ['sqrt', 'absolute']
        result = self.series.apply([np.sqrt, np.abs])
        assert_frame_equal(result, expected)
        result = self.series.transform(['sqrt', 'abs'])
        expected.columns = ['sqrt', 'abs']
        assert_frame_equal(result, expected)
        expected = pd.concat([f_sqrt, f_abs], axis=1)
        expected.columns = ['foo', 'bar']
        expected = expected.unstack().rename('series')
        result = self.series.apply({
            'foo': np.sqrt,
            'bar': np.abs,
        })
        assert_series_equal(result.reindex_like(expected), expected)