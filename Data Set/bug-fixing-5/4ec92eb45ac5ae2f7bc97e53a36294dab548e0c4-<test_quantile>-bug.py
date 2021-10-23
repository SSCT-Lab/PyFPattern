def test_quantile(self):
    from numpy import percentile
    q = self.tsframe.quantile(0.1, axis=0)
    assert (q['A'] == percentile(self.tsframe['A'], 10))
    tm.assert_index_equal(q.index, self.tsframe.columns)
    q = self.tsframe.quantile(0.9, axis=1)
    assert (q['2000-01-17'] == percentile(self.tsframe.loc['2000-01-17'], 90))
    tm.assert_index_equal(q.index, self.tsframe.index)
    q = DataFrame({
        'x': [],
        'y': [],
    }).quantile(0.1, axis=0)
    assert (np.isnan(q['x']) and np.isnan(q['y']))
    df = DataFrame({
        'col1': ['A', 'A', 'B', 'B'],
        'col2': [1, 2, 3, 4],
    })
    rs = df.quantile(0.5)
    xp = df.median().rename(0.5)
    assert_series_equal(rs, xp)
    df = DataFrame({
        'A': [1, 2, 3],
        'B': [2, 3, 4],
    }, index=[1, 2, 3])
    result = df.quantile(0.5, axis=1)
    expected = Series([1.5, 2.5, 3.5], index=[1, 2, 3], name=0.5)
    assert_series_equal(result, expected)
    result = df.quantile([0.5, 0.75], axis=1)
    expected = DataFrame({
        1: [1.5, 1.75],
        2: [2.5, 2.75],
        3: [3.5, 3.75],
    }, index=[0.5, 0.75])
    assert_frame_equal(result, expected, check_index_type=True)
    df = DataFrame([[1, 2, 3], ['a', 'b', 4]])
    result = df.quantile(0.5, axis=1)
    expected = Series([3.0, 4.0], index=[0, 1], name=0.5)
    assert_series_equal(result, expected)