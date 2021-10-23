

def test_multioutput_regression():
    y_true = np.array([[1, 0, 0, 1], [0, 1, 1, 1], [1, 1, 0, 1]])
    y_pred = np.array([[0, 0, 0, 1], [1, 0, 1, 1], [0, 0, 0, 1]])
    error = mean_squared_error(y_true, y_pred)
    assert_almost_equal(error, ((((1.0 / 3) + (2.0 / 3)) + (2.0 / 3)) / 4.0))
    error = mean_squared_error(y_true, y_pred, squared=False)
    assert_almost_equal(error, 0.645, decimal=2)
    error = mean_squared_log_error(y_true, y_pred)
    assert_almost_equal(error, 0.2, decimal=2)
    error = mean_absolute_error(y_true, y_pred)
    assert_almost_equal(error, ((((1.0 / 3) + (2.0 / 3)) + (2.0 / 3)) / 4.0))
    error = r2_score(y_true, y_pred, multioutput='variance_weighted')
    assert_almost_equal(error, (1.0 - (5.0 / 2)))
    error = r2_score(y_true, y_pred, multioutput='uniform_average')
    assert_almost_equal(error, (- 0.875))
