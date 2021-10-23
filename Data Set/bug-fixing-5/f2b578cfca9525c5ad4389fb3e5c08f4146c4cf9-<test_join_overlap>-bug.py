def test_join_overlap(frame):
    df1 = frame.loc[:, ['A', 'B', 'C']]
    df2 = frame.loc[:, ['B', 'C', 'D']]
    joined = df1.join(df2, lsuffix='_df1', rsuffix='_df2')
    df1_suf = df1.loc[:, ['B', 'C']].add_suffix('_df1')
    df2_suf = df2.loc[:, ['B', 'C']].add_suffix('_df2')
    no_overlap = frame.loc[:, ['A', 'D']]
    expected = df1_suf.join(df2_suf).join(no_overlap)
    tm.assert_frame_equal(joined, expected.loc[:, joined.columns])