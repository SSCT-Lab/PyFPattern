@pytest.mark.parametrize('arg', ['path', 'header', 'both'])
def test_to_csv_deprecation(self, arg):
    with ensure_clean() as path:
        if (arg == 'path'):
            kwargs = dict(path=path, header=False)
        elif (arg == 'header'):
            kwargs = dict(path_or_buf=path)
        else:
            kwargs = dict(path=path)
        with tm.assert_produces_warning(FutureWarning):
            self.ts.to_csv(**kwargs)
            ts = self.read_csv(path)
            assert_series_equal(self.ts, ts, check_names=False)