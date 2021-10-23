def test_from_csv(self, datetime_series, string_series):
    with ensure_clean() as path:
        datetime_series.to_csv(path, header=False)
        ts = self.read_csv(path)
        assert_series_equal(datetime_series, ts, check_names=False)
        assert (ts.name is None)
        assert (ts.index.name is None)
        with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
            depr_ts = Series.from_csv(path)
            assert_series_equal(depr_ts, ts)
        datetime_series.to_csv(path, header=True)
        ts_h = self.read_csv(path, header=0)
        assert (ts_h.name == 'ts')
        string_series.to_csv(path, header=False)
        series = self.read_csv(path)
        assert_series_equal(string_series, series, check_names=False)
        assert (series.name is None)
        assert (series.index.name is None)
        string_series.to_csv(path, header=True)
        series_h = self.read_csv(path, header=0)
        assert (series_h.name == 'series')
        with open(path, 'w') as outfile:
            outfile.write('1998-01-01|1.0\n1999-01-01|2.0')
        series = self.read_csv(path, sep='|')
        check_series = Series({
            datetime(1998, 1, 1): 1.0,
            datetime(1999, 1, 1): 2.0,
        })
        assert_series_equal(check_series, series)
        series = self.read_csv(path, sep='|', parse_dates=False)
        check_series = Series({
            '1998-01-01': 1.0,
            '1999-01-01': 2.0,
        })
        assert_series_equal(check_series, series)