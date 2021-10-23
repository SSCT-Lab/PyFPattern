def test_fill_corner(self):
    mf = self.mixed_frame
    mf.loc[(mf.index[5:20], 'foo')] = np.nan
    mf.loc[(mf.index[(- 10):], 'A')] = np.nan
    filled = self.mixed_frame.fillna(value=0)
    assert (filled.loc[(filled.index[5:20], 'foo')] == 0).all()
    del self.mixed_frame['foo']
    empty_float = self.frame.reindex(columns=[])
    result = empty_float.fillna(value=0)