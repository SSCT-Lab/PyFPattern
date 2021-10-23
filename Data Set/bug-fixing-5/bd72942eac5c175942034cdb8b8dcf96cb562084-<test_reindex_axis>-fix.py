def test_reindex_axis(self, float_frame, int_frame):
    cols = ['A', 'B', 'E']
    with tm.assert_produces_warning(FutureWarning) as m:
        reindexed1 = int_frame.reindex_axis(cols, axis=1)
        assert ('reindex' in str(m[0].message))
    reindexed2 = int_frame.reindex(columns=cols)
    assert_frame_equal(reindexed1, reindexed2)
    rows = int_frame.index[0:5]
    with tm.assert_produces_warning(FutureWarning) as m:
        reindexed1 = int_frame.reindex_axis(rows, axis=0)
        assert ('reindex' in str(m[0].message))
    reindexed2 = int_frame.reindex(index=rows)
    assert_frame_equal(reindexed1, reindexed2)
    msg = "No axis named 2 for object type <class 'pandas.core.frame.DataFrame'>"
    with pytest.raises(ValueError, match=msg):
        int_frame.reindex_axis(rows, axis=2)
    cols = float_frame.columns.copy()
    with tm.assert_produces_warning(FutureWarning) as m:
        newFrame = float_frame.reindex_axis(cols, axis=1)
        assert ('reindex' in str(m[0].message))
    assert_frame_equal(newFrame, float_frame)