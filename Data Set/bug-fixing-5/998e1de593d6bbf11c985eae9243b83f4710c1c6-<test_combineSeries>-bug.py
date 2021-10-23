def test_combineSeries(self):
    series = self.frame.xs(self.frame.index[0])
    added = (self.frame + series)
    for (key, s) in compat.iteritems(added):
        assert_series_equal(s, (self.frame[key] + series[key]))
    larger_series = series.to_dict()
    larger_series['E'] = 1
    larger_series = Series(larger_series)
    larger_added = (self.frame + larger_series)
    for (key, s) in compat.iteritems(self.frame):
        assert_series_equal(larger_added[key], (s + series[key]))
    assert ('E' in larger_added)
    assert np.isnan(larger_added['E']).all()
    added = (self.mixed_float + series)
    _check_mixed_float(added)
    added = (self.mixed_float + series.astype('float32'))
    _check_mixed_float(added, dtype=dict(C=None))
    added = (self.mixed_float + series.astype('float16'))
    _check_mixed_float(added, dtype=dict(C=None))
    ts = self.tsframe['A']
    added = self.tsframe.add(ts, axis='index')
    for (key, col) in compat.iteritems(self.tsframe):
        result = (col + ts)
        assert_series_equal(added[key], result, check_names=False)
        assert (added[key].name == key)
        if (col.name == ts.name):
            assert (result.name == 'A')
        else:
            assert (result.name is None)
    smaller_frame = self.tsframe[:(- 5)]
    smaller_added = smaller_frame.add(ts, axis='index')
    tm.assert_index_equal(smaller_added.index, self.tsframe.index)
    smaller_ts = ts[:(- 5)]
    smaller_added2 = self.tsframe.add(smaller_ts, axis='index')
    assert_frame_equal(smaller_added, smaller_added2)
    result = self.tsframe.add(ts[:0], axis='index')
    expected = DataFrame(np.nan, index=self.tsframe.index, columns=self.tsframe.columns)
    assert_frame_equal(result, expected)
    result = self.tsframe[:0].add(ts, axis='index')
    expected = DataFrame(np.nan, index=self.tsframe.index, columns=self.tsframe.columns)
    assert_frame_equal(result, expected)
    frame = self.tsframe[:1].reindex(columns=[])
    result = frame.mul(ts, axis='index')
    assert (len(result) == len(ts))