def test_apply_axis1(self):
    d = self.frame.index[0]
    tapplied = self.frame.apply(np.mean, axis=1)
    assert (tapplied[d] == np.mean(self.frame.xs(d)))