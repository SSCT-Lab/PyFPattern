def test_comment_used(self, engine, ext):
    df = DataFrame({
        'A': ['one', '#one', 'one'],
        'B': ['two', 'two', '#two'],
    })
    df.to_excel(self.path, 'test_c')
    expected = DataFrame({
        'A': ['one', None, 'one'],
        'B': ['two', None, None],
    })
    result = pd.read_excel(self.path, 'test_c', comment='#', index_col=0)
    tm.assert_frame_equal(result, expected)