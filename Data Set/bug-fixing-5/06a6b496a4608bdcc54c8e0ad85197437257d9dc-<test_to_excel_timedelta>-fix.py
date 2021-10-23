def test_to_excel_timedelta(self, path):
    df = DataFrame(np.random.randint((- 10), 10, size=(20, 1)), columns=['A'], dtype=np.int64)
    expected = df.copy()
    df['new'] = df['A'].apply((lambda x: timedelta(seconds=x)))
    expected['new'] = expected['A'].apply((lambda x: (timedelta(seconds=x).total_seconds() / float(86400))))
    df.to_excel(path, 'test1')
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(expected, recons)