def test_no_copy_blocks(self):
    df = DataFrame(self.frame, copy=True)
    column = df.columns[0]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        blocks = df.as_blocks(copy=False)
    for (dtype, _df) in blocks.items():
        if (column in _df):
            _df.loc[:, column] = (_df[column] + 1)
    assert _df[column].equals(df[column])