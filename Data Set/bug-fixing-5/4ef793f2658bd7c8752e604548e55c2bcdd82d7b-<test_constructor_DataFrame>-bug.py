def test_constructor_DataFrame(self):
    df = DataFrame(self.frame)
    tm.assert_frame_equal(df, self.frame)
    df_casted = DataFrame(self.frame, dtype=np.int64)
    assert (df_casted.values.dtype == np.int64)