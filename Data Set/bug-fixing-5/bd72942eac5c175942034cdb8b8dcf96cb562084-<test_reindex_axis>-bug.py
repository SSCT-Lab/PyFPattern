def test_reindex_axis(self):
    cols = ['A', 'B', 'E']
    with tm.assert_produces_warning(FutureWarning) as m:
        reindexed1 = self.intframe.reindex_axis(cols, axis=1)
        assert ('reindex' in str(m[0].message))
    reindexed2 = self.intframe.reindex(columns=cols)
    assert_frame_equal(reindexed1, reindexed2)
    rows = self.intframe.index[0:5]
    with tm.assert_produces_warning(FutureWarning) as m:
        reindexed1 = self.intframe.reindex_axis(rows, axis=0)
        assert ('reindex' in str(m[0].message))
    reindexed2 = self.intframe.reindex(index=rows)
    assert_frame_equal(reindexed1, reindexed2)
    msg = "No axis named 2 for object type <class 'pandas.core.frame.DataFrame'>"
    with pytest.raises(ValueError, match=msg):
        self.intframe.reindex_axis(rows, axis=2)
    cols = self.frame.columns.copy()
    with tm.assert_produces_warning(FutureWarning) as m:
        newFrame = self.frame.reindex_axis(cols, axis=1)
        assert ('reindex' in str(m[0].message))
    assert_frame_equal(newFrame, self.frame)