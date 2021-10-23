def test_excel_roundtrip_datetime(self, merge_cells, tsframe, engine, ext):
    tsf = tsframe.copy()
    tsf.index = [x.date() for x in tsframe.index]
    tsf.to_excel(self.path, 'test1', merge_cells=merge_cells)
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=0)
    tm.assert_frame_equal(tsframe, recons)