def test_combineSeries(self, float_frame, mixed_float_frame, mixed_int_frame, datetime_frame):
    series = float_frame.xs(float_frame.index[0])
    added = (float_frame + series)
    for (key, s) in compat.iteritems(added):
        assert_series_equal(s, (float_frame[key] + series[key]))
    larger_series = series.to_dict()
    larger_series['E'] = 1
    larger_series = Series(larger_series)
    larger_added = (float_frame + larger_series)
    for (key, s) in compat.iteritems(float_frame):
        assert_series_equal(larger_added[key], (s + series[key]))
    assert ('E' in larger_added)
    assert np.isnan(larger_added['E']).all()
    added = (mixed_float_frame + series)
    _check_mixed_float(added)
    added = (mixed_float_frame + series.astype('float32'))
    _check_mixed_float(added, dtype=dict(C=None))
    added = (mixed_float_frame + series.astype('float16'))
    _check_mixed_float(added, dtype=dict(C=None))
    ts = datetime_frame['A']
    added = datetime_frame.add(ts, axis='index')
    for (key, col) in compat.iteritems(datetime_frame):
        result = (col + ts)
        assert_series_equal(added[key], result, check_names=False)
        assert (added[key].name == key)
        if (col.name == ts.name):
            assert (result.name == 'A')
        else:
            assert (result.name is None)
    smaller_frame = datetime_frame[:(- 5)]
    smaller_added = smaller_frame.add(ts, axis='index')
    tm.assert_index_equal(smaller_added.index, datetime_frame.index)
    smaller_ts = ts[:(- 5)]
    smaller_added2 = datetime_frame.add(smaller_ts, axis='index')
    assert_frame_equal(smaller_added, smaller_added2)
    result = datetime_frame.add(ts[:0], axis='index')
    expected = DataFrame(np.nan, index=datetime_frame.index, columns=datetime_frame.columns)
    assert_frame_equal(result, expected)
    result = datetime_frame[:0].add(ts, axis='index')
    expected = DataFrame(np.nan, index=datetime_frame.index, columns=datetime_frame.columns)
    assert_frame_equal(result, expected)
    frame = datetime_frame[:1].reindex(columns=[])
    result = frame.mul(ts, axis='index')
    assert (len(result) == len(ts))