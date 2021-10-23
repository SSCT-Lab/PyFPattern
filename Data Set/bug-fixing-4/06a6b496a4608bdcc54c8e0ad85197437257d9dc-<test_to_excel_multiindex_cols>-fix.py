def test_to_excel_multiindex_cols(self, merge_cells, frame, path):
    arrays = np.arange((len(frame.index) * 2)).reshape(2, (- 1))
    new_index = MultiIndex.from_arrays(arrays, names=['first', 'second'])
    frame.index = new_index
    new_cols_index = MultiIndex.from_tuples([(40, 1), (40, 2), (50, 1), (50, 2)])
    frame.columns = new_cols_index
    header = [0, 1]
    if (not merge_cells):
        header = 0
    frame.to_excel(path, 'test1', merge_cells=merge_cells)
    reader = ExcelFile(path)
    df = pd.read_excel(reader, 'test1', header=header, index_col=[0, 1])
    if (not merge_cells):
        fm = frame.columns.format(sparsify=False, adjoin=False, names=False)
        frame.columns = ['.'.join(map(str, q)) for q in zip(*fm)]
    tm.assert_frame_equal(frame, df)