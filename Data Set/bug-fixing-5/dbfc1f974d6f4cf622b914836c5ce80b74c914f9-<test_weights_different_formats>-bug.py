def test_weights_different_formats():
    weights = [1, 1, 1, 2, 2, 2, 3, 3, 3, 1, 1, 1, 2, 2, 2, 3, 3]
    (yield (check_weights_as_formats, weights))
    (yield (check_weights_as_formats, np.asarray(weights)))
    (yield (check_weights_as_formats, pd.Series(weights)))