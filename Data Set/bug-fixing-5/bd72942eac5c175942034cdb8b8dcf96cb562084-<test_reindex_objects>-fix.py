def test_reindex_objects(self, float_string_frame):
    reindexed = float_string_frame.reindex(columns=['foo', 'A', 'B'])
    assert ('foo' in reindexed)
    reindexed = float_string_frame.reindex(columns=['A', 'B'])
    assert ('foo' not in reindexed)