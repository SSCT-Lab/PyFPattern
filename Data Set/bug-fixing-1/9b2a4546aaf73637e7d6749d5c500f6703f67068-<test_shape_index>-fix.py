

def test_shape_index():
    square = np.zeros((5, 5))
    square[(2, 2)] = 4
    with expected_warnings(['divide by zero|\\A\\Z', 'invalid value|\\A\\Z']):
        s = shape_index(square, sigma=0.1)
    assert_almost_equal(s, np.array([[np.nan, np.nan, (- 0.5), np.nan, np.nan], [np.nan, 0, np.nan, 0, np.nan], [(- 0.5), np.nan, (- 1), np.nan, (- 0.5)], [np.nan, 0, np.nan, 0, np.nan], [np.nan, np.nan, (- 0.5), np.nan, np.nan]]))
