def test_excel_roundtrip_datetime(self, merge_cells, tsframe, path):
    tsf = tsframe.copy()
    tsf.index = [x.date() for x in tsframe.index]
    tsf.to_excel(path, 'test1', merge_cells=merge_cells)
    reader = ExcelFile(path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(tsframe, recons)