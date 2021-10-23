def test_apply_deprecate_reduce(self, empty_frame):
    x = []
    with tm.assert_produces_warning(FutureWarning):
        empty_frame.apply(x.append, axis=1, reduce=True)