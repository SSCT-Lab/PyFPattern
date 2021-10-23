def test_basics_with_nan(self, frame, path):
    frame = frame.copy()
    frame['A'][:5] = np.nan
    frame.to_excel(path, 'test1')
    frame.to_excel(path, 'test1', columns=['A', 'B'])
    frame.to_excel(path, 'test1', header=False)
    frame.to_excel(path, 'test1', index=False)