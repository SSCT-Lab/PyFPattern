def test_invert_int8():
    dtype = 'int8'
    image = np.zeros((3, 3), dtype=dtype)
    (lower_dtype_limit, upper_dtype_limit) = dtype_limits(image, clip_negative=False)
    image[1, :] = lower_dtype_limit
    image[2, :] = upper_dtype_limit
    expected = np.zeros((3, 3), dtype=dtype)
    expected[2, :] = lower_dtype_limit
    expected[1, :] = upper_dtype_limit
    expected[0, :] = (- 1)
    result = invert(image)
    assert_array_equal(expected, result)