def test_to_excel_multiindex_dates(self, merge_cells, engine, ext, tsframe):
    new_index = [tsframe.index, np.arange(len(tsframe.index))]
    tsframe.index = MultiIndex.from_arrays(new_index)
    tsframe.index.names = ['time', 'foo']
    tsframe.to_excel(self.path, 'test1', merge_cells=merge_cells)
    reader = ExcelFile(self.path)
    recons = pd.read_excel(reader, 'test1', index_col=[0, 1])
    tm.assert_frame_equal(tsframe, recons)
    assert (recons.index.names == ('time', 'foo'))