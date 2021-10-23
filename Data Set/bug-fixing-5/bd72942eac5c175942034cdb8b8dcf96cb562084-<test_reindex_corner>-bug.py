def test_reindex_corner(self):
    index = Index(['a', 'b', 'c'])
    dm = self.empty.reindex(index=[1, 2, 3])
    reindexed = dm.reindex(columns=index)
    tm.assert_index_equal(reindexed.columns, index)
    smaller = self.intframe.reindex(columns=['A', 'B', 'E'])
    assert (smaller['E'].dtype == np.float64)