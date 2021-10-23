def test_merged_cell_custom_objects(self, engine, merge_cells, ext):
    mi = MultiIndex.from_tuples([(pd.Period('2018'), pd.Period('2018Q1')), (pd.Period('2018'), pd.Period('2018Q2'))])
    expected = DataFrame(np.ones((2, 2)), columns=mi)
    expected.to_excel(self.path)
    result = pd.read_excel(self.path, header=[0, 1], index_col=0, convert_float=False)
    expected.columns.set_levels([[str(i) for i in mi.levels[0]], [str(i) for i in mi.levels[1]]], level=[0, 1], inplace=True)
    expected.index = expected.index.astype(np.float64)
    tm.assert_frame_equal(expected, result)