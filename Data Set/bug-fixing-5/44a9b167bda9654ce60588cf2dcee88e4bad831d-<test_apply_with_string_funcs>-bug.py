@pytest.mark.parametrize('func', ['sum', 'mean', 'min', 'max', 'std'])
@pytest.mark.parametrize('args,kwds', [pytest.param([], {
    
}, id='no_args_or_kwds'), pytest.param([1], {
    
}, id='axis_from_args'), pytest.param([], {
    'axis': 1,
}, id='axis_from_kwds'), pytest.param([], {
    'numeric_only': True,
}, id='optional_kwds'), pytest.param([1, None], {
    'numeric_only': True,
}, id='args_and_kwds')])
def test_apply_with_string_funcs(self, func, args, kwds):
    result = self.frame.apply(func, *args, **kwds)
    expected = getattr(self.frame, func)(*args, **kwds)
    tm.assert_series_equal(result, expected)