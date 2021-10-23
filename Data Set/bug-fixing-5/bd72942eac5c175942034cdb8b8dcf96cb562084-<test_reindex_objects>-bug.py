def test_reindex_objects(self):
    reindexed = self.mixed_frame.reindex(columns=['foo', 'A', 'B'])
    assert ('foo' in reindexed)
    reindexed = self.mixed_frame.reindex(columns=['A', 'B'])
    assert ('foo' not in reindexed)