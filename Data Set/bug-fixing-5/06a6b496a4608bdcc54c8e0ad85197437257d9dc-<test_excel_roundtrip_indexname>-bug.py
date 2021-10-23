def test_excel_roundtrip_indexname(self, merge_cells, engine, ext):
    df = DataFrame(np.random.randn(10, 4))
    df.index.name = 'foo'
    df.to_excel(self.path, merge_cells=merge_cells)
    xf = ExcelFile(self.path)
    result = pd.read_excel(xf, xf.sheet_names[0], index_col=0)
    tm.assert_frame_equal(result, df)
    assert (result.index.name == 'foo')