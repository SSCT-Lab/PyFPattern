def test_invalid_columns(self, engine, ext):
    write_frame = DataFrame({
        'A': [1, 1, 1],
        'B': [2, 2, 2],
    })
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        write_frame.to_excel(self.path, 'test1', columns=['B', 'C'])
    expected = write_frame.reindex(columns=['B', 'C'])
    read_frame = pd.read_excel(self.path, 'test1', index_col=0)
    tm.assert_frame_equal(expected, read_frame)
    with pytest.raises(KeyError, match="'passes columns are not ALL present dataframe'"):
        write_frame.to_excel(self.path, 'test1', columns=['C', 'D'])