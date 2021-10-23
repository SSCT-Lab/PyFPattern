def test_join_index_series(frame):
    df = frame.copy()
    s = df.pop(frame.columns[(- 1)])
    joined = df.join(s)
    tm.assert_frame_equal(joined, frame, check_names=False)
    s.name = None
    with pytest.raises(ValueError, match='must have a name'):
        df.join(s)