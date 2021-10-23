def test_constructor_from_items(self, float_frame, float_string_frame):
    items = [(c, float_frame[c]) for c in float_frame.columns]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(items)
    tm.assert_frame_equal(recons, float_frame)
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(items, columns=['C', 'B', 'A'])
    tm.assert_frame_equal(recons, float_frame.loc[:, ['C', 'B', 'A']])
    row_items = [(idx, float_string_frame.xs(idx)) for idx in float_string_frame.index]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(row_items, columns=float_string_frame.columns, orient='index')
    tm.assert_frame_equal(recons, float_string_frame)
    assert (recons['A'].dtype == np.float64)
    msg = "Must pass columns with orient='index'"
    with pytest.raises(TypeError, match=msg):
        with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
            DataFrame.from_items(row_items, orient='index')
    arr = construct_1d_object_array_from_listlike(([('bar', 'baz')] * len(float_string_frame)))
    float_string_frame['foo'] = arr
    row_items = [(idx, list(float_string_frame.xs(idx))) for idx in float_string_frame.index]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(row_items, columns=float_string_frame.columns, orient='index')
    tm.assert_frame_equal(recons, float_string_frame)
    assert isinstance(recons['foo'][0], tuple)
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        rs = DataFrame.from_items([('A', [1, 2, 3]), ('B', [4, 5, 6])], orient='index', columns=['one', 'two', 'three'])
    xp = DataFrame([[1, 2, 3], [4, 5, 6]], index=['A', 'B'], columns=['one', 'two', 'three'])
    tm.assert_frame_equal(rs, xp)