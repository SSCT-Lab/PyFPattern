def test_to_excel_float_format(self, engine, ext):
    df = DataFrame([[0.123456, 0.234567, 0.567567], [12.32112, 123123.2, 321321.2]], index=['A', 'B'], columns=['X', 'Y', 'Z'])
    df.to_excel(self.path, 'test1', float_format='%.2f')
    reader = ExcelFile(self.path)
    result = pd.read_excel(reader, 'test1', index_col=0)
    expected = DataFrame([[0.12, 0.23, 0.57], [12.32, 123123.2, 321321.2]], index=['A', 'B'], columns=['X', 'Y', 'Z'])
    tm.assert_frame_equal(result, expected)