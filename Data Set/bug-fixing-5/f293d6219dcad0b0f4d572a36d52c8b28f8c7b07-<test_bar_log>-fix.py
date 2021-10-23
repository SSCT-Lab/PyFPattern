@slow
def test_bar_log(self):
    expected = np.array([1.0, 10.0, 100.0, 1000.0])
    if (not self.mpl_le_1_2_1):
        expected = np.hstack((0.1, expected, 10000.0))
    ax = Series([200, 500]).plot.bar(log=True)
    tm.assert_numpy_array_equal(ax.yaxis.get_ticklocs(), expected)
    tm.close()
    ax = Series([200, 500]).plot.barh(log=True)
    tm.assert_numpy_array_equal(ax.xaxis.get_ticklocs(), expected)
    tm.close()
    expected = np.array([0.001, 0.01, 0.1, 1.0])
    if (not self.mpl_le_1_2_1):
        expected = np.hstack((0.0001, expected, 10.0))
    if self.mpl_ge_2_0_0:
        expected = np.hstack((1e-05, expected))
    ax = Series([0.1, 0.01, 0.001]).plot(log=True, kind='bar')
    ymin = (0.0007943282347242822 if self.mpl_ge_2_0_0 else 0.001)
    ymax = (0.12589254117941673 if self.mpl_ge_2_0_0 else 0.1)
    res = ax.get_ylim()
    self.assertAlmostEqual(res[0], ymin)
    self.assertAlmostEqual(res[1], ymax)
    tm.assert_numpy_array_equal(ax.yaxis.get_ticklocs(), expected)
    tm.close()
    ax = Series([0.1, 0.01, 0.001]).plot(log=True, kind='barh')
    res = ax.get_xlim()
    self.assertAlmostEqual(res[0], ymin)
    self.assertAlmostEqual(res[1], ymax)
    tm.assert_numpy_array_equal(ax.xaxis.get_ticklocs(), expected)