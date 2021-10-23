def test_comparisons(self, simple_frame, float_frame):
    df1 = tm.makeTimeDataFrame()
    df2 = tm.makeTimeDataFrame()
    row = simple_frame.xs('a')
    ndim_5 = np.ones((df1.shape + (1, 1, 1)))

    def test_comp(func):
        result = func(df1, df2)
        tm.assert_numpy_array_equal(result.values, func(df1.values, df2.values))
        with pytest.raises(ValueError, match='dim must be <= 2'):
            func(df1, ndim_5)
        result2 = func(simple_frame, row)
        tm.assert_numpy_array_equal(result2.values, func(simple_frame.values, row.values))
        result3 = func(float_frame, 0)
        tm.assert_numpy_array_equal(result3.values, func(float_frame.values, 0))
        msg = 'Can only compare identically-labeled DataFrame'
        with pytest.raises(ValueError, match=msg):
            func(simple_frame, simple_frame[:2])
    test_comp(operator.eq)
    test_comp(operator.ne)
    test_comp(operator.lt)
    test_comp(operator.gt)
    test_comp(operator.ge)
    test_comp(operator.le)