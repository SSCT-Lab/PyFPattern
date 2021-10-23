def test_apply(self):
    with np.errstate(all='ignore'):
        applied = self.frame.apply(np.sqrt)
        tm.assert_series_equal(np.sqrt(self.frame['A']), applied['A'])
        applied = self.frame.apply(np.mean)
        assert (applied['A'] == np.mean(self.frame['A']))
        d = self.frame.index[0]
        applied = self.frame.apply(np.mean, axis=1)
        assert (applied[d] == np.mean(self.frame.xs(d)))
        assert (applied.index is self.frame.index)
    df = DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], index=['a', 'a', 'c'])
    pytest.raises(ValueError, df.apply, (lambda x: x), 2)
    df = DataFrame({
        'c0': ['A', 'A', 'B', 'B'],
        'c1': ['C', 'C', 'D', 'D'],
    })
    df = df.apply((lambda ts: ts.astype('category')))
    assert (df.shape == (4, 2))
    assert isinstance(df['c0'].dtype, CategoricalDtype)
    assert isinstance(df['c1'].dtype, CategoricalDtype)