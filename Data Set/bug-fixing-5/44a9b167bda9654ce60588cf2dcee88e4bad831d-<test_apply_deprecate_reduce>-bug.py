def test_apply_deprecate_reduce(self):
    x = []
    with tm.assert_produces_warning(FutureWarning):
        self.empty.apply(x.append, axis=1, reduce=True)