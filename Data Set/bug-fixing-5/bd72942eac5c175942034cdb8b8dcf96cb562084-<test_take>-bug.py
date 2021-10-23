def test_take(self):
    order = [3, 1, 2, 0]
    for df in [self.frame]:
        result = df.take(order, axis=0)
        expected = df.reindex(df.index.take(order))
        assert_frame_equal(result, expected)
        result = df.take(order, axis=1)
        expected = df.loc[:, ['D', 'B', 'C', 'A']]
        assert_frame_equal(result, expected, check_names=False)
    order = [2, 1, (- 1)]
    for df in [self.frame]:
        result = df.take(order, axis=0)
        expected = df.reindex(df.index.take(order))
        assert_frame_equal(result, expected)
        with tm.assert_produces_warning(FutureWarning):
            result = df.take(order, convert=True, axis=0)
            assert_frame_equal(result, expected)
        with tm.assert_produces_warning(FutureWarning):
            result = df.take(order, convert=False, axis=0)
            assert_frame_equal(result, expected)
        result = df.take(order, axis=1)
        expected = df.loc[:, ['C', 'B', 'D']]
        assert_frame_equal(result, expected, check_names=False)
    msg = 'indices are out-of-bounds'
    with pytest.raises(IndexError, match=msg):
        df.take([3, 1, 2, 30], axis=0)
    with pytest.raises(IndexError, match=msg):
        df.take([3, 1, 2, (- 31)], axis=0)
    with pytest.raises(IndexError, match=msg):
        df.take([3, 1, 2, 5], axis=1)
    with pytest.raises(IndexError, match=msg):
        df.take([3, 1, 2, (- 5)], axis=1)
    order = [4, 1, 2, 0, 3]
    for df in [self.mixed_frame]:
        result = df.take(order, axis=0)
        expected = df.reindex(df.index.take(order))
        assert_frame_equal(result, expected)
        result = df.take(order, axis=1)
        expected = df.loc[:, ['foo', 'B', 'C', 'A', 'D']]
        assert_frame_equal(result, expected)
    order = [4, 1, (- 2)]
    for df in [self.mixed_frame]:
        result = df.take(order, axis=0)
        expected = df.reindex(df.index.take(order))
        assert_frame_equal(result, expected)
        result = df.take(order, axis=1)
        expected = df.loc[:, ['foo', 'B', 'D']]
        assert_frame_equal(result, expected)
    order = [1, 2, 0, 3]
    for df in [self.mixed_float, self.mixed_int]:
        result = df.take(order, axis=0)
        expected = df.reindex(df.index.take(order))
        assert_frame_equal(result, expected)
        result = df.take(order, axis=1)
        expected = df.loc[:, ['B', 'C', 'A', 'D']]
        assert_frame_equal(result, expected)