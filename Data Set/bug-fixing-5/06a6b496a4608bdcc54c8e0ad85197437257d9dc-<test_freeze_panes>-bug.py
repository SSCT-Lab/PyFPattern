def test_freeze_panes(self, engine, ext):
    expected = DataFrame([[1, 2], [3, 4]], columns=['col1', 'col2'])
    expected.to_excel(self.path, 'Sheet1', freeze_panes=(1, 1))
    result = pd.read_excel(self.path, index_col=0)
    tm.assert_frame_equal(result, expected)