def test_comment_default(self, engine, ext):
    df = DataFrame({
        'A': ['one', '#one', 'one'],
        'B': ['two', 'two', '#two'],
    })
    df.to_excel(self.path, 'test_c')
    result1 = pd.read_excel(self.path, 'test_c')
    result2 = pd.read_excel(self.path, 'test_c', comment=None)
    tm.assert_frame_equal(result1, result2)