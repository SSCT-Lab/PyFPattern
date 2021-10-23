def test_colaliases(self, frame, path):
    frame = frame.copy()
    frame['A'][:5] = np.nan
    frame.to_excel(path, 'test1')
    frame.to_excel(path, 'test1', columns=['A', 'B'])
    frame.to_excel(path, 'test1', header=False)
    frame.to_excel(path, 'test1', index=False)
    col_aliases = Index(['AA', 'X', 'Y', 'Z'])
    frame.to_excel(path, 'test1', header=col_aliases)
    reader = ExcelFile(path)
    rs = pd.read_excel(reader, 'test1', index_col=0)
    xp = frame.copy()
    xp.columns = col_aliases
    tm.assert_frame_equal(xp, rs)