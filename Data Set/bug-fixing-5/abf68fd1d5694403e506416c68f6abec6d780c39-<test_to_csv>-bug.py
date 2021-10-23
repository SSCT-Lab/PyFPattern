def test_to_csv(self):
    import io
    with ensure_clean() as path:
        self.ts.to_csv(path, header=False)
        with io.open(path, newline=None) as f:
            lines = f.readlines()
        assert (lines[1] != '\n')
        self.ts.to_csv(path, index=False, header=False)
        arr = np.loadtxt(path)
        assert_almost_equal(arr, self.ts.values)