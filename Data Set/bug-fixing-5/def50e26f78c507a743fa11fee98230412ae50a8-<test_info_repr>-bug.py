def test_info_repr(self):
    max_rows = 60
    max_cols = 20
    (h, w) = ((max_rows + 1), (max_cols - 1))
    df = DataFrame({k: np.arange(1, (1 + h)) for k in np.arange(w)})
    assert has_vertically_truncated_repr(df)
    with option_context('display.large_repr', 'info'):
        assert has_info_repr(df)
    (h, w) = ((max_rows - 1), (max_cols + 1))
    df = DataFrame({k: np.arange(1, (1 + h)) for k in np.arange(w)})
    assert has_horizontally_truncated_repr(df)
    with option_context('display.large_repr', 'info', 'display.max_columns', max_cols):
        assert has_info_repr(df)