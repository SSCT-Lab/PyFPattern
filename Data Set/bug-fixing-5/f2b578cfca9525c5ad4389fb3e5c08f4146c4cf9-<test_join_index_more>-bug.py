def test_join_index_more(frame):
    af = frame.loc[:, ['A', 'B']]
    bf = frame.loc[::2, ['C', 'D']]
    expected = af.copy()
    expected['C'] = frame['C'][::2]
    expected['D'] = frame['D'][::2]
    result = af.join(bf)
    tm.assert_frame_equal(result, expected)
    result = af.join(bf, how='right')
    tm.assert_frame_equal(result, expected[::2])
    result = bf.join(af, how='right')
    tm.assert_frame_equal(result, expected.loc[:, result.columns])