def test_reindex_like(self, float_frame):
    other = float_frame.reindex(index=float_frame.index[:10], columns=['C', 'B'])
    assert_frame_equal(other, float_frame.reindex_like(other))