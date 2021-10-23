def test_from_csv_deprecation(self):
    with ensure_clean() as path:
        self.ts.to_csv(path, header=False)
        with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
            ts = self.read_csv(path)
            depr_ts = Series.from_csv(path)
            assert_series_equal(depr_ts, ts)