def assert_series_equal(left, right, check_dtype=True, check_index_type='equiv', check_series_type=True, check_less_precise=False, check_names=True, check_exact=False, check_datetimelike_compat=False, check_categorical=True, obj='Series'):
    "\n    Check that left and right Series are equal.\n\n    Parameters\n    ----------\n    left : Series\n    right : Series\n    check_dtype : bool, default True\n        Whether to check the Series dtype is identical.\n    check_index_type : bool / string {'equiv'}, default 'equiv'\n        Whether to check the Index class, dtype and inferred_type\n        are identical.\n    check_series_type : bool, default True\n        Whether to check the Series class is identical.\n    check_less_precise : bool or int, default False\n        Specify comparison precision. Only used when check_exact is False.\n        5 digits (False) or 3 digits (True) after decimal points are compared.\n        If int, then specify the digits to compare.\n\n        When comparing two numbers, if the first number has magnitude less\n        than 1e-5, we compare the two numbers directly and check whether\n        they are equivalent within the specified precision. Otherwise, we\n        compare the **ratio** of the second number to the first number and\n        check whether it is equivalent to 1 within the specified precision.\n    check_names : bool, default True\n        Whether to check the Series and Index names attribute.\n    check_exact : bool, default False\n        Whether to compare number exactly.\n    check_datetimelike_compat : bool, default False\n        Compare datetime-like which is comparable ignoring dtype.\n    check_categorical : bool, default True\n        Whether to compare internal Categorical exactly.\n    obj : str, default 'Series'\n        Specify object name being compared, internally used to show appropriate\n        assertion message.\n    "
    __tracebackhide__ = True
    _check_isinstance(left, right, Series)
    if check_series_type:
        assert isinstance(left, type(right))
    if (len(left) != len(right)):
        msg1 = '{len}, {left}'.format(len=len(left), left=left.index)
        msg2 = '{len}, {right}'.format(len=len(right), right=right.index)
        raise_assert_detail(obj, 'Series length are different', msg1, msg2)
    assert_index_equal(left.index, right.index, exact=check_index_type, check_names=check_names, check_less_precise=check_less_precise, check_exact=check_exact, check_categorical=check_categorical, obj='{obj}.index'.format(obj=obj))
    if check_dtype:
        if (is_categorical_dtype(left) and is_categorical_dtype(right) and (not check_categorical)):
            pass
        else:
            assert_attr_equal('dtype', left, right)
    if check_exact:
        assert_numpy_array_equal(left._internal_get_values(), right._internal_get_values(), check_dtype=check_dtype, obj='{obj}'.format(obj=obj))
    elif check_datetimelike_compat:
        if (needs_i8_conversion(left) or needs_i8_conversion(right)):
            if (not Index(left.values).equals(Index(right.values))):
                msg = '[datetimelike_compat=True] {left} is not equal to {right}.'.format(left=left.values, right=right.values)
                raise AssertionError(msg)
        else:
            assert_numpy_array_equal(left._internal_get_values(), right._internal_get_values(), check_dtype=check_dtype)
    elif (is_interval_dtype(left) or is_interval_dtype(right)):
        assert_interval_array_equal(left.array, right.array)
    elif (is_extension_array_dtype(left.dtype) and is_datetime64tz_dtype(left.dtype)):
        assert is_extension_array_dtype(right.dtype)
        assert_extension_array_equal(left._values, right._values)
    elif (is_extension_array_dtype(left) and (not is_categorical_dtype(left)) and is_extension_array_dtype(right) and (not is_categorical_dtype(right))):
        assert_extension_array_equal(left.array, right.array)
    else:
        _testing.assert_almost_equal(left._internal_get_values(), right._internal_get_values(), check_less_precise=check_less_precise, check_dtype=check_dtype, obj='{obj}'.format(obj=obj))
    if check_names:
        assert_attr_equal('name', left, right, obj=obj)
    if check_categorical:
        if (is_categorical_dtype(left) or is_categorical_dtype(right)):
            assert_categorical_equal(left.values, right.values, obj='{obj} category'.format(obj=obj))