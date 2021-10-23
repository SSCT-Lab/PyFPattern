def test_maybe_promote_any_with_bytes(any_numpy_dtype_reduced, bytes_dtype, box):
    dtype = np.dtype(any_numpy_dtype_reduced)
    fill_dtype = np.dtype(bytes_dtype)
    (boxed, box_dtype) = box
    if (not issubclass(dtype.type, np.bytes_)):
        if (boxed and ((box_dtype == 'bytes') or (box_dtype is None)) and (not (is_string_dtype(dtype) or (dtype == bool)))):
            pytest.xfail('does not upcast to object')
    fill_value = b'abc'
    box_dtype = (fill_dtype if (box_dtype == 'bytes') else box_dtype)
    expected_dtype = np.dtype(np.object_)
    exp_val_for_scalar = np.array([fill_value], dtype=expected_dtype)[0]
    exp_val_for_array = np.nan
    _check_promote(dtype, fill_value, boxed, box_dtype, expected_dtype, exp_val_for_scalar, exp_val_for_array)