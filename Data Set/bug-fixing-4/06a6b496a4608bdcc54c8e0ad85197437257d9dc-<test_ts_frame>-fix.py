def test_ts_frame(self, tsframe, path):
    df = tsframe
    df.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(df, recons)