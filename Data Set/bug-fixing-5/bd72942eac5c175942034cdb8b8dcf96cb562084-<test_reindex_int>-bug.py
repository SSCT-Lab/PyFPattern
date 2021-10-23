def test_reindex_int(self):
    smaller = self.intframe.reindex(self.intframe.index[::2])
    assert (smaller['A'].dtype == np.int64)
    bigger = smaller.reindex(self.intframe.index)
    assert (bigger['A'].dtype == np.float64)
    smaller = self.intframe.reindex(columns=['A', 'B'])
    assert (smaller['A'].dtype == np.int64)