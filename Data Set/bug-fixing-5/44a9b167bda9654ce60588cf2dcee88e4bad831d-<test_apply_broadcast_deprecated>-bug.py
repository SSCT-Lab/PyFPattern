def test_apply_broadcast_deprecated(self):
    with tm.assert_produces_warning(FutureWarning):
        self.frame.apply(np.mean, broadcast=True)