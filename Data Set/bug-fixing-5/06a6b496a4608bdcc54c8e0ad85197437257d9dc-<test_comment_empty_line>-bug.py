def test_comment_empty_line(self, engine, ext):
    df = DataFrame({
        'a': ['1', '#2'],
        'b': ['2', '3'],
    })
    df.to_excel(self.path, index=False)
    expected = DataFrame({
        'a': [1],
        'b': [2],
    })
    result = pd.read_excel(self.path, comment='#')
    tm.assert_frame_equal(result, expected)