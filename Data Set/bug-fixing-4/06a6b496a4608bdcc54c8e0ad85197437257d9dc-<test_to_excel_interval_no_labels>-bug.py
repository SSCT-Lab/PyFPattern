def test_to_excel_interval_no_labels(self, engine, ext):
    df = DataFrame(np.random.randint((- 10), 10, size=(20, 1)), dtype=np.int64)
    expected = df.copy()
    df['new'] = pd.cut(df[0], 10)
    expected['new'] = pd.cut(expected[0], 10).astype(str)
    df.to_excel(self.path, 'test1')
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(expected, recons)