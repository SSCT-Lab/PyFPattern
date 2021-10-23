def test_ops_properties_basic(self):
    msg = "'Series' object has no attribute '{}'"
    for op in ['year', 'day', 'second', 'weekday']:
        with pytest.raises(AttributeError, match=msg.format(op)):
            getattr(self.dt_series, op)
    s = Series(dict(year=2000, month=1, day=10))
    assert (s.year == 2000)
    assert (s.month == 1)
    assert (s.day == 10)
    msg = "'Series' object has no attribute 'weekday'"
    with pytest.raises(AttributeError, match=msg):
        s.weekday