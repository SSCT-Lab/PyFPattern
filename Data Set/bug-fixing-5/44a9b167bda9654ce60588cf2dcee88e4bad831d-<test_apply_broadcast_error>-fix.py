def test_apply_broadcast_error(self, int_frame_const_col):
    df = int_frame_const_col
    with pytest.raises(ValueError):
        df.apply((lambda x: np.array([1, 2]).reshape((- 1), 2)), axis=1, result_type='broadcast')
    with pytest.raises(ValueError):
        df.apply((lambda x: [1, 2]), axis=1, result_type='broadcast')
    with pytest.raises(ValueError):
        df.apply((lambda x: Series([1, 2])), axis=1, result_type='broadcast')