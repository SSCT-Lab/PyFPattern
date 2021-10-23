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
    ax = Series([0.1, 0.01, 0.001]).plot(log=True, kind='bar')
    ymax = (0.12589254117941673 if self.mpl_ge_2_0_0 else 0.1)
    self.assertEqual(ax.get_ylim(), (0.001, ymax))
    tm.assert_numpy_array_equal(ax.yaxis.get_ticklocs(), expected)
    tm.close()
    ax = Series([0.1, 0.01, 0.001]).plot(log=True, kind='barh')
    self.assertEqual(ax.get_xlim(), (0.001, ymax))
    tm.assert_numpy_array_equal(ax.xaxis.get_ticklocs(), expected)