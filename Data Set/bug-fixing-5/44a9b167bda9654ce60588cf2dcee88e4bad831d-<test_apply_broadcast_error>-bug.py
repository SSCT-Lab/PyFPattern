def test_apply_broadcast_error(self):
    df = DataFrame((np.tile(np.arange(3, dtype='int64'), 6).reshape(6, (- 1)) + 1), columns=['A', 'B', 'C'])
    with pytest.raises(ValueError):
        df.apply((lambda x: np.array([1, 2]).reshape((- 1), 2)), axis=1, result_type='broadcast')
    with pytest.raises(ValueError):
        df.apply((lambda x: [1, 2]), axis=1, result_type='broadcast')
    with pytest.raises(ValueError):
        df.apply((lambda x: Series([1, 2])), axis=1, result_type='broadcast')