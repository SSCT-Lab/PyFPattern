def test_to_excel_interval_labels(self, path):
    df = DataFrame(np.random.randint((- 10), 10, size=(20, 1)), dtype=np.int64)
    expected = df.copy()
    intervals = pd.cut(df[0], 10, labels=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
    df['new'] = intervals
    expected['new'] = pd.Series(list(intervals))
    df.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(expected, recons)