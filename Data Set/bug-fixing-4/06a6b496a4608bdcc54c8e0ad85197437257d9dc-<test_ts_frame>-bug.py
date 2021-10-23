def test_ts_frame(self, tsframe, engine, ext):
    df = tsframe
    df.to_excel(self.path, 'test1')
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(df, recons)