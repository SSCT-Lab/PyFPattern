def test_copy_blocks(self, float_frame):
    df = DataFrame(float_frame, copy=True)
    column = df.columns[0]
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        blocks = df.as_blocks()
    for (dtype, _df) in blocks.items():
        if (column in _df):
            _df.loc[:, column] = (_df[column] + 1)
    assert (not _df[column].equals(df[column]))