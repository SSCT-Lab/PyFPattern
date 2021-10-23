def test_append_many(self, datetime_series):
    pieces = [datetime_series[:5], datetime_series[5:10], datetime_series[10:]]
    result = pieces[0].append(pieces[1:])
    assert_series_equal(result, datetime_series)