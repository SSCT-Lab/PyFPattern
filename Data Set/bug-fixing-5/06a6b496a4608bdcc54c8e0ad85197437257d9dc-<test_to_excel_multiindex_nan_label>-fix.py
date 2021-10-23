def test_to_excel_multiindex_nan_label(self, merge_cells, path):
    df = pd.DataFrame({
        'A': [None, 2, 3],
        'B': [10, 20, 30],
        'C': np.random.sample(3),
    })
    df = df.set_index(['A', 'B'])
    df.to_excel(path, merge_cells=merge_cells)
    df1 = pd.read_excel(path, index_col=[0, 1])
    tm.assert_frame_equal(df, df1)