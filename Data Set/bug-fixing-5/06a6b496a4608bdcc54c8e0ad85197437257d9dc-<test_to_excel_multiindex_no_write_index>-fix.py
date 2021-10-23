def test_to_excel_multiindex_no_write_index(self, path):
    frame1 = DataFrame({
        'a': [10, 20],
        'b': [30, 40],
        'c': [50, 60],
    })
    frame2 = frame1.copy()
    multi_index = MultiIndex.from_tuples([(70, 80), (90, 100)])
    frame2.index = multi_index
    frame2.to_excel(path, 'test1', index=False)
    reader = ExcelFile(path)
    frame3 = pd.read_excel(reader, 'test1')
    tm.assert_frame_equal(frame1, frame3)