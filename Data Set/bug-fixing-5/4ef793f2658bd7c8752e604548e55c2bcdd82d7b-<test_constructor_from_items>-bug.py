def test_constructor_from_items(self):
    items = [(c, self.frame[c]) for c in self.frame.columns]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(items)
    tm.assert_frame_equal(recons, self.frame)
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(items, columns=['C', 'B', 'A'])
    tm.assert_frame_equal(recons, self.frame.loc[:, ['C', 'B', 'A']])
    row_items = [(idx, self.mixed_frame.xs(idx)) for idx in self.mixed_frame.index]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(row_items, columns=self.mixed_frame.columns, orient='index')
    tm.assert_frame_equal(recons, self.mixed_frame)
    assert (recons['A'].dtype == np.float64)
    msg = "Must pass columns with orient='index'"
    with pytest.raises(TypeError, match=msg):
        with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
            DataFrame.from_items(row_items, orient='index')
    arr = construct_1d_object_array_from_listlike(([('bar', 'baz')] * len(self.mixed_frame)))
    self.mixed_frame['foo'] = arr
    row_items = [(idx, list(self.mixed_frame.xs(idx))) for idx in self.mixed_frame.index]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        recons = DataFrame.from_items(row_items, columns=self.mixed_frame.columns, orient='index')
    tm.assert_frame_equal(recons, self.mixed_frame)
    assert isinstance(recons['foo'][0], tuple)
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        rs = DataFrame.from_items([('A', [1, 2, 3]), ('B', [4, 5, 6])], orient='index', columns=['one', 'two', 'three'])
    xp = DataFrame([[1, 2, 3], [4, 5, 6]], index=['A', 'B'], columns=['one', 'two', 'three'])
    tm.assert_frame_equal(rs, xp)