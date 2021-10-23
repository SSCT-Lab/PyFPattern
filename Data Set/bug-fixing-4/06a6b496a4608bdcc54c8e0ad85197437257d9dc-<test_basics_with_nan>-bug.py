def test_basics_with_nan(self, engine, ext, frame):
    frame = frame.copy()
    frame['A'][:5] = np.nan
    frame.to_excel(self.path, 'test1')
    frame.to_excel(self.path, 'test1', columns=['A', 'B'])
    frame.to_excel(self.path, 'test1', header=False)
    frame.to_excel(self.path, 'test1', index=False)