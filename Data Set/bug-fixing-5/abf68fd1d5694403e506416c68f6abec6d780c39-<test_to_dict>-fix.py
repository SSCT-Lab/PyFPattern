@pytest.mark.parametrize('mapping', (dict, collections.defaultdict(list), collections.OrderedDict))
def test_to_dict(self, mapping, datetime_series):
    tm.assert_series_equal(Series(datetime_series.to_dict(mapping), name='ts'), datetime_series)
    from_method = Series(datetime_series.to_dict(collections.Counter))
    from_constructor = Series(collections.Counter(datetime_series.iteritems()))
    tm.assert_series_equal(from_method, from_constructor)