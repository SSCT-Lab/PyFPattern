def test_constructor_orient(self, float_string_frame):
    data_dict = float_string_frame.T._series
    recons = DataFrame.from_dict(data_dict, orient='index')
    expected = float_string_frame.sort_index()
    tm.assert_frame_equal(recons, expected)
    a = {
        'hi': [32, 3, 3],
        'there': [3, 5, 3],
    }
    rs = DataFrame.from_dict(a, orient='index')
    xp = DataFrame.from_dict(a).T.reindex(list(a.keys()))
    tm.assert_frame_equal(rs, xp)