def test_comment_arg(self, engine, ext):
    df = DataFrame({
        'A': ['one', '#one', 'one'],
        'B': ['two', 'two', '#two'],
    })
    df.to_excel(self.path, 'test_c')
    result1 = pd.read_excel(self.path, 'test_c', index_col=0)
    result1.iloc[(1, 0)] = None
    result1.iloc[(1, 1)] = None
    result1.iloc[(2, 1)] = None
    result2 = pd.read_excel(self.path, 'test_c', comment='#', index_col=0)
    tm.assert_frame_equal(result1, result2)