def test_round(self, datetime_series):
    datetime_series.index.name = 'index_name'
    result = datetime_series.round(2)
    expected = Series(np.round(datetime_series.values, 2), index=datetime_series.index, name='ts')
    assert_series_equal(result, expected)
    assert (result.name == datetime_series.name)