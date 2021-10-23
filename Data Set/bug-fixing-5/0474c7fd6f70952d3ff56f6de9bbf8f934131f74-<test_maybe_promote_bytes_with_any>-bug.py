def test_maybe_promote_bytes_with_any(bytes_dtype, any_numpy_dtype_reduced, box):
    dtype = np.dtype(bytes_dtype)
    fill_dtype = np.dtype(any_numpy_dtype_reduced)
    (boxed, box_dtype) = box
    if issubclass(fill_dtype.type, np.bytes_):
        if ((not boxed) or (box_dtype == object)):
            pytest.xfail('falsely upcasts to object')
        else:
            pytest.xfail('wrong missing value marker')
    elif (boxed and (box_dtype is None)):
        pytest.xfail('does not upcast to object')
    fill_value = np.array([1], dtype=fill_dtype)[0]
    expected_dtype = (dtype if issubclass(fill_dtype.type, np.bytes_) else np.dtype(object))
    exp_val_for_scalar = fill_value
    exp_val_for_array = (None if issubclass(fill_dtype.type, np.bytes_) else np.nan)
    _check_promote(dtype, fill_value, boxed, box_dtype, expected_dtype, exp_val_for_scalar, exp_val_for_array)