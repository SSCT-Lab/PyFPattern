def test_excel_sheet_by_name_raise(self, path):
    import xlrd
    gt = DataFrame(np.random.randn(10, 2))
    gt.to_excel(path)
    xl = ExcelFile(path)
    df = pd.read_excel(xl, 0, index_col=0)
    tm.assert_frame_equal(gt, df)
    with pytest.raises(xlrd.XLRDError):
        pd.read_excel(xl, '0')