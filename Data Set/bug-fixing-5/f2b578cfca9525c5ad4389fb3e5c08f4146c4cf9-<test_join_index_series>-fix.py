def test_join_index_series(float_frame):
    df = float_frame.copy()
    s = df.pop(float_frame.columns[(- 1)])
    joined = df.join(s)
    tm.assert_frame_equal(joined, float_frame, check_names=False)
    s.name = None
    with pytest.raises(ValueError, match='must have a name'):
        df.join(s)