def test_to_excel_multiindex(self, merge_cells, frame, path):
    arrays = np.arange((len(frame.index) * 2)).reshape(2, (- 1))
    new_index = MultiIndex.from_arrays(arrays, names=['first', 'second'])
    frame.index = new_index
    frame.to_excel(path, 'test1', header=False)
    frame.to_excel(path, 'test1', columns=['A', 'B'])
    frame.to_excel(path, 'test1', merge_cells=merge_cells)
    reader = ExcelFile(path)
    df = pd.read_excel(reader, 'test1', index_col=[0, 1])
    tm.assert_frame_equal(frame, df)