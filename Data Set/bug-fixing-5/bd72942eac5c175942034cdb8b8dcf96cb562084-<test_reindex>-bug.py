def test_reindex(self):
    newFrame = self.frame.reindex(self.ts1.index)
    for col in newFrame.columns:
        for (idx, val) in newFrame[col].items():
            if (idx in self.frame.index):
                if np.isnan(val):
                    assert np.isnan(self.frame[col][idx])
                else:
                    assert (val == self.frame[col][idx])
            else:
                assert np.isnan(val)
    for (col, series) in newFrame.items():
        assert tm.equalContents(series.index, newFrame.index)
    emptyFrame = self.frame.reindex(Index([]))
    assert (len(emptyFrame.index) == 0)
    nonContigFrame = self.frame.reindex(self.ts1.index[::2])
    for col in nonContigFrame.columns:
        for (idx, val) in nonContigFrame[col].items():
            if (idx in self.frame.index):
                if np.isnan(val):
                    assert np.isnan(self.frame[col][idx])
                else:
                    assert (val == self.frame[col][idx])
            else:
                assert np.isnan(val)
    for (col, series) in nonContigFrame.items():
        assert tm.equalContents(series.index, nonContigFrame.index)
    newFrame = self.frame.reindex(self.frame.index, copy=False)
    assert (newFrame.index is self.frame.index)
    newFrame = self.frame.reindex([])
    assert newFrame.empty
    assert (len(newFrame.columns) == len(self.frame.columns))
    newFrame = self.frame.reindex([])
    newFrame = newFrame.reindex(self.frame.index)
    assert (len(newFrame.index) == len(self.frame.index))
    assert (len(newFrame.columns) == len(self.frame.columns))
    newFrame = self.frame.reindex(list(self.ts1.index))
    tm.assert_index_equal(newFrame.index, self.ts1.index)
    result = self.frame.reindex()
    assert_frame_equal(result, self.frame)
    assert (result is not self.frame)