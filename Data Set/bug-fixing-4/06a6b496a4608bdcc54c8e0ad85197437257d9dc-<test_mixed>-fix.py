def test_mixed(self, frame, path):
    mixed_frame = frame.copy()
    mixed_frame['foo'] = 'bar'
    mixed_frame.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(mixed_frame, recons)