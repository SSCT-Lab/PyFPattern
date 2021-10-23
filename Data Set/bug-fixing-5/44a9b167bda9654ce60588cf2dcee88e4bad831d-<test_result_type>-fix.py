def test_result_type(self, int_frame_const_col):
    df = int_frame_const_col
    result = df.apply((lambda x: [1, 2, 3]), axis=1, result_type='expand')
    expected = df.copy()
    expected.columns = [0, 1, 2]
    assert_frame_equal(result, expected)
    result = df.apply((lambda x: [1, 2]), axis=1, result_type='expand')
    expected = df[['A', 'B']].copy()
    expected.columns = [0, 1]
    assert_frame_equal(result, expected)
    result = df.apply((lambda x: [1, 2, 3]), axis=1, result_type='broadcast')
    expected = df.copy()
    assert_frame_equal(result, expected)
    columns = ['other', 'col', 'names']
    result = df.apply((lambda x: Series([1, 2, 3], index=columns)), axis=1, result_type='broadcast')
    expected = df.copy()
    assert_frame_equal(result, expected)
    result = df.apply((lambda x: Series([1, 2, 3], index=x.index)), axis=1)
    expected = df.copy()
    assert_frame_equal(result, expected)
    columns = ['other', 'col', 'names']
    result = df.apply((lambda x: Series([1, 2, 3], index=columns)), axis=1)
    expected = df.copy()
    expected.columns = columns
    assert_frame_equal(result, expected)