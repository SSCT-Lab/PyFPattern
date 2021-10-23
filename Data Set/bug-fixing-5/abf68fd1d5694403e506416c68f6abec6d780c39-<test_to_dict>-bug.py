@pytest.mark.parametrize('mapping', (dict, collections.defaultdict(list), collections.OrderedDict))
def test_to_dict(self, mapping):
    ts = TestData().ts
    tm.assert_series_equal(Series(ts.to_dict(mapping), name='ts'), ts)
    from_method = Series(ts.to_dict(collections.Counter))
    from_constructor = Series(collections.Counter(ts.iteritems()))
    tm.assert_series_equal(from_method, from_constructor)