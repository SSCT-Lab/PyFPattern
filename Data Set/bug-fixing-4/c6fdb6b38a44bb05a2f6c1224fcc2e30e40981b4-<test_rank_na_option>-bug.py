def test_rank_na_option(self):
    rankdata = pytest.importorskip('scipy.stats.rankdata')
    self.frame['A'][::2] = np.nan
    self.frame['B'][::3] = np.nan
    self.frame['C'][::4] = np.nan
    self.frame['D'][::5] = np.nan
    ranks0 = self.frame.rank(na_option='bottom')
    ranks1 = self.frame.rank(1, na_option='bottom')
    fvals = self.frame.fillna(np.inf).values
    exp0 = np.apply_along_axis(rankdata, 0, fvals)
    exp1 = np.apply_along_axis(rankdata, 1, fvals)
    tm.assert_almost_equal(ranks0.values, exp0)
    tm.assert_almost_equal(ranks1.values, exp1)
    ranks0 = self.frame.rank(na_option='top')
    ranks1 = self.frame.rank(1, na_option='top')
    fval0 = self.frame.fillna((self.frame.min() - 1).to_dict()).values
    fval1 = self.frame.T
    fval1 = fval1.fillna((fval1.min() - 1).to_dict()).T
    fval1 = fval1.fillna(np.inf).values
    exp0 = np.apply_along_axis(rankdata, 0, fval0)
    exp1 = np.apply_along_axis(rankdata, 1, fval1)
    tm.assert_almost_equal(ranks0.values, exp0)
    tm.assert_almost_equal(ranks1.values, exp1)
    ranks0 = self.frame.rank(na_option='top', ascending=False)
    ranks1 = self.frame.rank(1, na_option='top', ascending=False)
    fvals = self.frame.fillna(np.inf).values
    exp0 = np.apply_along_axis(rankdata, 0, (- fvals))
    exp1 = np.apply_along_axis(rankdata, 1, (- fvals))
    tm.assert_almost_equal(ranks0.values, exp0)
    tm.assert_almost_equal(ranks1.values, exp1)
    ranks0 = self.frame.rank(na_option='bottom', ascending=False)
    ranks1 = self.frame.rank(1, na_option='bottom', ascending=False)
    fval0 = self.frame.fillna((self.frame.min() - 1).to_dict()).values
    fval1 = self.frame.T
    fval1 = fval1.fillna((fval1.min() - 1).to_dict()).T
    fval1 = fval1.fillna(np.inf).values
    exp0 = np.apply_along_axis(rankdata, 0, (- fval0))
    exp1 = np.apply_along_axis(rankdata, 1, (- fval1))
    tm.assert_numpy_array_equal(ranks0.values, exp0)
    tm.assert_numpy_array_equal(ranks1.values, exp1)
    msg = "na_option must be one of 'keep', 'top', or 'bottom'"
    with pytest.raises(ValueError, match=msg):
        self.frame.rank(na_option='bad', ascending=False)
    with pytest.raises(ValueError, match=msg):
        self.frame.rank(na_option=True, ascending=False)