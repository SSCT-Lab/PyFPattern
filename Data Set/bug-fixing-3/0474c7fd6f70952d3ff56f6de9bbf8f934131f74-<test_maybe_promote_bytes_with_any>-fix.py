def test_maybe_promote_bytes_with_any(bytes_dtype, any_numpy_dtype_reduced, box):
    dtype = np.dtype(bytes_dtype)
    fill_dtype = np.dtype(any_numpy_dtype_reduced)
    (boxed, box_dtype) = box
    fill_value = np.array([1], dtype=fill_dtype)[0]
    expected_dtype = np.dtype(np.object_)
    exp_val_for_scalar = fill_value
    exp_val_for_array = np.nan
    _check_promote(dtype, fill_value, boxed, box_dtype, expected_dtype, exp_val_for_scalar, exp_val_for_array)