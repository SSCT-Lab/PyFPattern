def test_apply_axis1(self, float_frame):
    d = float_frame.index[0]
    tapplied = float_frame.apply(np.mean, axis=1)
    assert (tapplied[d] == np.mean(float_frame.xs(d)))