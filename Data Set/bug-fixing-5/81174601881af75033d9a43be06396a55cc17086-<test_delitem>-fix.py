def test_delitem(self, float_frame):
    del float_frame['A']
    assert ('A' not in float_frame)