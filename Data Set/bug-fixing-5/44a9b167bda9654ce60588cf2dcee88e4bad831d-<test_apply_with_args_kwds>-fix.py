def test_apply_with_args_kwds(self, float_frame):

    def add_some(x, howmuch=0):
        return (x + howmuch)

    def agg_and_add(x, howmuch=0):
        return (x.mean() + howmuch)

    def subtract_and_divide(x, sub, divide=1):
        return ((x - sub) / divide)
    result = float_frame.apply(add_some, howmuch=2)
    exp = float_frame.apply((lambda x: (x + 2)))
    assert_frame_equal(result, exp)
    result = float_frame.apply(agg_and_add, howmuch=2)
    exp = float_frame.apply((lambda x: (x.mean() + 2)))
    assert_series_equal(result, exp)
    res = float_frame.apply(subtract_and_divide, args=(2,), divide=2)
    exp = float_frame.apply((lambda x: ((x - 2.0) / 2.0)))
    assert_frame_equal(res, exp)