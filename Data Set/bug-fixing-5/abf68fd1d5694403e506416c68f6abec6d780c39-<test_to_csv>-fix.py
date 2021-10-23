def test_to_csv(self, datetime_series):
    import io
    with ensure_clean() as path:
        datetime_series.to_csv(path, header=False)
        with io.open(path, newline=None) as f:
            lines = f.readlines()
        assert (lines[1] != '\n')
        datetime_series.to_csv(path, index=False, header=False)
        arr = np.loadtxt(path)
        assert_almost_equal(arr, datetime_series.values)