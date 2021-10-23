@pytest.mark.parametrize('use_headers', [True, False])
@pytest.mark.parametrize('r_idx_nlevels', [1, 2, 3])
@pytest.mark.parametrize('c_idx_nlevels', [1, 2, 3])
def test_excel_010_hemstring(self, merge_cells, engine, ext, c_idx_nlevels, r_idx_nlevels, use_headers):

    def roundtrip(data, header=True, parser_hdr=0, index=True):
        data.to_excel(self.path, header=header, merge_cells=merge_cells, index=index)
        xf = ExcelFile(self.path)
        return pd.read_excel(xf, xf.sheet_names[0], header=parser_hdr)
    parser_header = (0 if use_headers else None)
    res = roundtrip(DataFrame([0]), use_headers, parser_header)
    assert (res.shape == (1, 2))
    assert (res.iloc[(0, 0)] is not np.nan)
    nrows = 5
    ncols = 3
    from pandas.util.testing import makeCustomDataframe as mkdf
    df = mkdf(nrows, ncols, r_idx_nlevels=r_idx_nlevels, c_idx_nlevels=c_idx_nlevels)
    if (c_idx_nlevels > 1):
        with pytest.raises(NotImplementedError):
            roundtrip(df, use_headers, index=False)
    else:
        res = roundtrip(df, use_headers)
        if use_headers:
            assert (res.shape == (nrows, (ncols + r_idx_nlevels)))
        else:
            assert (res.shape == ((nrows - 1), (ncols + r_idx_nlevels)))
        for r in range(len(res.index)):
            for c in range(len(res.columns)):
                assert (res.iloc[(r, c)] is not np.nan)