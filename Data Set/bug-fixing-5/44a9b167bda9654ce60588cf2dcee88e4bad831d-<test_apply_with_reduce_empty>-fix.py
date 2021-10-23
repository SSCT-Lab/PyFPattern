def test_apply_with_reduce_empty(self, empty_frame):
    x = []
    result = empty_frame.apply(x.append, axis=1, result_type='expand')
    assert_frame_equal(result, empty_frame)
    result = empty_frame.apply(x.append, axis=1, result_type='reduce')
    assert_series_equal(result, Series([], index=pd.Index([], dtype=object)))
    empty_with_cols = DataFrame(columns=['a', 'b', 'c'])
    result = empty_with_cols.apply(x.append, axis=1, result_type='expand')
    assert_frame_equal(result, empty_with_cols)
    result = empty_with_cols.apply(x.append, axis=1, result_type='reduce')
    assert_series_equal(result, Series([], index=pd.Index([], dtype=object)))
    assert (x == [])