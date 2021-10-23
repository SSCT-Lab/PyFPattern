def test_dropEmptyRows(self):
    N = len(self.frame.index)
    mat = np.random.randn(N)
    mat[:5] = np.nan
    frame = DataFrame({
        'foo': mat,
    }, index=self.frame.index)
    original = Series(mat, index=self.frame.index, name='foo')
    expected = original.dropna()
    (inplace_frame1, inplace_frame2) = (frame.copy(), frame.copy())
    smaller_frame = frame.dropna(how='all')
    assert_series_equal(frame['foo'], original)
    inplace_frame1.dropna(how='all', inplace=True)
    assert_series_equal(smaller_frame['foo'], expected)
    assert_series_equal(inplace_frame1['foo'], expected)
    smaller_frame = frame.dropna(how='all', subset=['foo'])
    inplace_frame2.dropna(how='all', subset=['foo'], inplace=True)
    assert_series_equal(smaller_frame['foo'], expected)
    assert_series_equal(inplace_frame2['foo'], expected)