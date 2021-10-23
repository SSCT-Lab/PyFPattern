def test_inf_roundtrip(self, engine, ext):
    df = DataFrame([(1, np.inf), (2, 3), (5, (- np.inf))])
    df.to_excel(self.path, 'test1')
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(df, recons)