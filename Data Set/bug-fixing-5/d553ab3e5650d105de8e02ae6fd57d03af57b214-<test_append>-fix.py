def test_append(self, datetime_series, string_series, object_series):
    appendedSeries = string_series.append(object_series)
    for (idx, value) in compat.iteritems(appendedSeries):
        if (idx in string_series.index):
            assert (value == string_series[idx])
        elif (idx in object_series.index):
            assert (value == object_series[idx])
        else:
            raise AssertionError('orphaned index!')
    pytest.raises(ValueError, datetime_series.append, datetime_series, verify_integrity=True)