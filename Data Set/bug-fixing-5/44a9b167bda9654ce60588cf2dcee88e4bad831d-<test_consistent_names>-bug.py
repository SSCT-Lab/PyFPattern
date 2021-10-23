def test_consistent_names(self):
    df = DataFrame((np.tile(np.arange(3, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['A', 'B', 'C'])
    result = df.apply((lambda x: Series([1, 2, 3], index=['test', 'other', 'cols'])), axis=1)
    expected = DataFrame((np.tile(np.arange(3, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['test', 'other', 'cols'])
    assert_frame_equal(result, expected)
    result = df.apply((lambda x: pd.Series([1, 2], index=['test', 'other'])), axis=1)
    expected = DataFrame((np.tile(np.arange(2, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['test', 'other'])
    assert_frame_equal(result, expected)