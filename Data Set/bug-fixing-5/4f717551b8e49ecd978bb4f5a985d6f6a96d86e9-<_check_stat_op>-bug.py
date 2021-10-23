def _check_stat_op(self, name, alternate, check_objects=False, check_allna=False):
    with pd.option_context('use_bottleneck', False):
        f = getattr(Series, name)
        self.series[5:15] = np.NaN
        if (name not in ['max', 'min']):
            ds = Series(date_range('1/1/2001', periods=10))
            pytest.raises(TypeError, f, ds)
        assert notna(f(self.series))
        assert isna(f(self.series, skipna=False))
        nona = self.series.dropna()
        assert_almost_equal(f(nona), alternate(nona.values))
        assert_almost_equal(f(self.series), alternate(nona.values))
        allna = (self.series * nan)
        if check_allna:
            assert np.isnan(f(allna))
        s = Series([1, 2, 3, None, 5])
        f(s)
        items = [0]
        items.extend(lrange((2 ** 40), ((2 ** 40) + 1000)))
        s = Series(items, dtype='int64')
        assert_almost_equal(float(f(s)), float(alternate(s.values)))
        if check_objects:
            s = Series(bdate_range('1/1/2000', periods=10))
            res = f(s)
            exp = alternate(s)
            assert (res == exp)
        if (name not in ['sum', 'min', 'max']):
            pytest.raises(TypeError, f, Series(list('abc')))
        pytest.raises(ValueError, f, self.series, axis=1)
        if ('numeric_only' in compat.signature(f).args):
            tm.assert_raises_regex(NotImplementedError, name, f, self.series, numeric_only=True)