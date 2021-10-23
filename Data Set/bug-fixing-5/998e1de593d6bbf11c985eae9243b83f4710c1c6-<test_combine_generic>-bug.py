def test_combine_generic(self):
    df1 = self.frame
    df2 = self.frame.loc[(self.frame.index[:(- 5)], ['A', 'B', 'C'])]
    combined = df1.combine(df2, np.add)
    combined2 = df2.combine(df1, np.add)
    assert combined['D'].isna().all()
    assert combined2['D'].isna().all()
    chunk = combined.loc[(combined.index[:(- 5)], ['A', 'B', 'C'])]
    chunk2 = combined2.loc[(combined2.index[:(- 5)], ['A', 'B', 'C'])]
    exp = (self.frame.loc[(self.frame.index[:(- 5)], ['A', 'B', 'C'])].reindex_like(chunk) * 2)
    assert_frame_equal(chunk, exp)
    assert_frame_equal(chunk2, exp)