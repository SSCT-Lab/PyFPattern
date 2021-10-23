def test_dropIncompleteRows(self):
    N = len(self.frame.index)
    mat = np.random.randn(N)
    mat[:5] = np.nan
    frame = DataFrame({
        'foo': mat,
    }, index=self.frame.index)
    frame['bar'] = 5
    original = Series(mat, index=self.frame.index, name='foo')
    (inp_frame1, inp_frame2) = (frame.copy(), frame.copy())
    smaller_frame = frame.dropna()
    assert_series_equal(frame['foo'], original)
    inp_frame1.dropna(inplace=True)
    exp = Series(mat[5:], index=self.frame.index[5:], name='foo')
    tm.assert_series_equal(smaller_frame['foo'], exp)
    tm.assert_series_equal(inp_frame1['foo'], exp)
    samesize_frame = frame.dropna(subset=['bar'])
    assert_series_equal(frame['foo'], original)
    assert (frame['bar'] == 5).all()
    inp_frame2.dropna(subset=['bar'], inplace=True)
    tm.assert_index_equal(samesize_frame.index, self.frame.index)
    tm.assert_index_equal(inp_frame2.index, self.frame.index)