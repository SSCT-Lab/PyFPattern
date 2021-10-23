def test_join_overlap(float_frame):
    df1 = float_frame.loc[:, ['A', 'B', 'C']]
    df2 = float_frame.loc[:, ['B', 'C', 'D']]
    joined = df1.join(df2, lsuffix='_df1', rsuffix='_df2')
    df1_suf = df1.loc[:, ['B', 'C']].add_suffix('_df1')
    df2_suf = df2.loc[:, ['B', 'C']].add_suffix('_df2')
    no_overlap = float_frame.loc[:, ['A', 'D']]
    expected = df1_suf.join(df2_suf).join(no_overlap)
    tm.assert_frame_equal(joined, expected.loc[:, joined.columns])