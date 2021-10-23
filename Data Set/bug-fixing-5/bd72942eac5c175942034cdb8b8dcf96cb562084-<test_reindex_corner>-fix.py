def test_reindex_corner(self, int_frame):
    index = Index(['a', 'b', 'c'])
    dm = DataFrame({
        
    }).reindex(index=[1, 2, 3])
    reindexed = dm.reindex(columns=index)
    tm.assert_index_equal(reindexed.columns, index)
    smaller = int_frame.reindex(columns=['A', 'B', 'E'])
    assert (smaller['E'].dtype == np.float64)