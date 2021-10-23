def test_mixed(self, engine, ext, frame):
    mixed_frame = frame.copy()
    mixed_frame['foo'] = 'bar'
    mixed_frame.to_excel(self.path, 'test1')
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(mixed_frame, recons)