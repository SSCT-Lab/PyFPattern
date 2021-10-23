def test_swapped_columns(self, path):
    write_frame = DataFrame({
        'A': [1, 1, 1],
        'B': [2, 2, 2],
    })
    write_frame.to_excel(path, 'test1', columns=['B', 'A'])
    read_frame = pd.read_excel(path, 'test1', header=0)
    tm.assert_series_equal(write_frame['A'], read_frame['A'])
    tm.assert_series_equal(write_frame['B'], read_frame['B'])