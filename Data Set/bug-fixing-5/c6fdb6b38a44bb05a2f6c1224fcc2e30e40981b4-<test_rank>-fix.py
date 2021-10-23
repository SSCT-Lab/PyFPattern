def test_rank(self, float_frame):
    rankdata = pytest.importorskip('scipy.stats.rankdata')
    float_frame['A'][::2] = np.nan
    float_frame['B'][::3] = np.nan
    float_frame['C'][::4] = np.nan
    float_frame['D'][::5] = np.nan
    ranks0 = float_frame.rank()
    ranks1 = float_frame.rank(1)
    mask = np.isnan(float_frame.values)
    fvals = float_frame.fillna(np.inf).values
    exp0 = np.apply_along_axis(rankdata, 0, fvals)
    exp0[mask] = np.nan
    exp1 = np.apply_along_axis(rankdata, 1, fvals)
    exp1[mask] = np.nan
    tm.assert_almost_equal(ranks0.values, exp0)
    tm.assert_almost_equal(ranks1.values, exp1)
    df = DataFrame(np.random.randint(0, 5, size=40).reshape((10, 4)))
    result = df.rank()
    exp = df.astype(float).rank()
    tm.assert_frame_equal(result, exp)
    result = df.rank(1)
    exp = df.astype(float).rank(1)
    tm.assert_frame_equal(result, exp)