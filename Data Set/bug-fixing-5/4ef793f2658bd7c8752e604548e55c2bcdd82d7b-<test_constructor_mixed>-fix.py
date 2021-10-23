def test_constructor_mixed(self, float_string_frame):
    (index, data) = tm.getMixedTypeDict()
    indexed_frame = DataFrame(data, index=index)
    unindexed_frame = DataFrame(data)
    assert (float_string_frame['foo'].dtype == np.object_)