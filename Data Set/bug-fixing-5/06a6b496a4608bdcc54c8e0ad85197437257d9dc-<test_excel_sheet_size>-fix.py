def test_excel_sheet_size(self, path):
    breaking_row_count = ((2 ** 20) + 1)
    breaking_col_count = ((2 ** 14) + 1)
    row_arr = np.zeros(shape=(breaking_row_count, 1))
    col_arr = np.zeros(shape=(1, breaking_col_count))
    row_df = pd.DataFrame(row_arr)
    col_df = pd.DataFrame(col_arr)
    msg = 'sheet is too large'
    with pytest.raises(ValueError, match=msg):
        row_df.to_excel(path)
    with pytest.raises(ValueError, match=msg):
        col_df.to_excel(path)