def test_modify_values(self, float_frame):
    float_frame.values[5] = 5
    assert (float_frame.values[5] == 5).all()
    float_frame['E'] = 7.0
    float_frame.values[6] = 6
    assert (float_frame.values[6] == 6).all()