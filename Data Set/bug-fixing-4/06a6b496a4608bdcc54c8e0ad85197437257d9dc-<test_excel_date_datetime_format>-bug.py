def test_excel_date_datetime_format(self, engine, ext):
    df = DataFrame([[date(2014, 1, 31), date(1999, 9, 24)], [datetime(1998, 5, 26, 23, 33, 4), datetime(2014, 2, 28, 13, 5, 13)]], index=['DATE', 'DATETIME'], columns=['X', 'Y'])
    df_expected = DataFrame([[datetime(2014, 1, 31), datetime(1999, 9, 24)], [datetime(1998, 5, 26, 23, 33, 4), datetime(2014, 2, 28, 13, 5, 13)]], index=['DATE', 'DATETIME'], columns=['X', 'Y'])
    with ensure_clean(ext) as filename2:
        writer1 = ExcelWriter(self.path)
        writer2 = ExcelWriter(filename2, date_format='DD.MM.YYYY', datetime_format='DD.MM.YYYY HH-MM-SS')
        df.to_excel(writer1, 'test1')
        df.to_excel(writer2, 'test1')
        writer1.close()
        writer2.close()
        reader1 = ExcelFile(self.path)
        reader2 = ExcelFile(filename2)
        rs1 = pd.read_excel(reader1, 'test1', index_col=0)
        rs2 = pd.read_excel(reader2, 'test1', index_col=0)
        tm.assert_frame_equal(rs1, rs2)
        tm.assert_frame_equal(rs2, df_expected)