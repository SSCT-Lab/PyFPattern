def test_reindex_int(self, int_frame):
    smaller = int_frame.reindex(int_frame.index[::2])
    assert (smaller['A'].dtype == np.int64)
    bigger = smaller.reindex(int_frame.index)
    assert (bigger['A'].dtype == np.float64)
    smaller = int_frame.reindex(columns=['A', 'B'])
    assert (smaller['A'].dtype == np.int64)