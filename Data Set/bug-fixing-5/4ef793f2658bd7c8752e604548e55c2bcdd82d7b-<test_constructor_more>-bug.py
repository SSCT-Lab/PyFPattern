def test_constructor_more(self):
    arr = np.random.randn(10)
    dm = DataFrame(arr, columns=['A'], index=np.arange(10))
    assert (dm.values.ndim == 2)
    arr = np.random.randn(0)
    dm = DataFrame(arr)
    assert (dm.values.ndim == 2)
    assert (dm.values.ndim == 2)
    dm = DataFrame(columns=['A', 'B'], index=np.arange(10))
    assert (dm.values.shape == (10, 2))
    dm = DataFrame(columns=['A', 'B'])
    assert (dm.values.shape == (0, 2))
    dm = DataFrame(index=np.arange(10))
    assert (dm.values.shape == (10, 0))
    mat = np.array(['foo', 'bar'], dtype=object).reshape(2, 1)
    with pytest.raises(ValueError, match='cast'):
        DataFrame(mat, index=[0, 1], columns=[0], dtype=float)
    dm = DataFrame(DataFrame(self.frame._series))
    tm.assert_frame_equal(dm, self.frame)
    dm = DataFrame({
        'A': np.ones(10, dtype=int),
        'B': np.ones(10, dtype=np.float64),
    }, index=np.arange(10))
    assert (len(dm.columns) == 2)
    assert (dm.values.dtype == np.float64)