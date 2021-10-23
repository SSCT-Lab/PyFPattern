def test_apply_broadcast_deprecated(self, float_frame):
    with tm.assert_produces_warning(FutureWarning):
        float_frame.apply(np.mean, broadcast=True)