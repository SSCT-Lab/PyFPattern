def test_pickle(self):
    unpickled = tm.round_trip_pickle(self.mixed_frame)
    assert_frame_equal(self.mixed_frame, unpickled)
    self.mixed_frame._data.ndim
    unpickled = tm.round_trip_pickle(self.empty)
    repr(unpickled)
    unpickled = tm.round_trip_pickle(self.tzframe)
    assert_frame_equal(self.tzframe, unpickled)