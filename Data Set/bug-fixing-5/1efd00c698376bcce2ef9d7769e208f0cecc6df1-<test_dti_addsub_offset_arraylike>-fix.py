@pytest.mark.parametrize('op', [operator.add, roperator.radd, operator.sub])
@pytest.mark.parametrize('names', [(None, None, None), ('foo', 'bar', None), ('foo', 'foo', 'foo')])
def test_dti_addsub_offset_arraylike(self, tz_naive_fixture, names, op, index_or_series):
    box = pd.Index
    other_box = index_or_series
    from .test_timedelta64 import get_upcast_box
    tz = tz_naive_fixture
    dti = pd.date_range('2017-01-01', periods=2, tz=tz, name=names[0])
    other = other_box([pd.offsets.MonthEnd(), pd.offsets.Day(n=2)], name=names[1])
    xbox = get_upcast_box(box, other)
    with tm.assert_produces_warning(PerformanceWarning, clear=[dtl]):
        res = op(dti, other)
    expected = DatetimeIndex([op(dti[n], other[n]) for n in range(len(dti))], name=names[2], freq='infer')
    expected = tm.box_expected(expected, xbox)
    tm.assert_equal(res, expected)