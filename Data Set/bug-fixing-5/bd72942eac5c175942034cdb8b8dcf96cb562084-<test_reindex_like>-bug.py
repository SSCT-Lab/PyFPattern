def test_reindex_like(self):
    other = self.frame.reindex(index=self.frame.index[:10], columns=['C', 'B'])
    assert_frame_equal(other, self.frame.reindex_like(other))