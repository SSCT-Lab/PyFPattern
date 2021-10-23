def test_constructor_mix_series_nonseries(self):
    df = DataFrame({
        'A': self.frame['A'],
        'B': list(self.frame['B']),
    }, columns=['A', 'B'])
    tm.assert_frame_equal(df, self.frame.loc[:, ['A', 'B']])
    msg = 'does not match index length'
    with pytest.raises(ValueError, match=msg):
        DataFrame({
            'A': self.frame['A'],
            'B': list(self.frame['B'])[:(- 2)],
        })