def assert_almost_equal(left, right, check_dtype='equiv', check_less_precise=False, **kwargs):
    "\n    Check that the left and right objects are approximately equal.\n\n    By approximately equal, we refer to objects that are numbers or that\n    contain numbers which may be equivalent to specific levels of precision.\n\n    Parameters\n    ----------\n    left : object\n    right : object\n    check_dtype : bool or {'equiv'}, default 'equiv'\n        Check dtype if both a and b are the same type. If 'equiv' is passed in,\n        then `RangeIndex` and `Int64Index` are also considered equivalent\n        when doing type checking.\n    check_less_precise : bool or int, default False\n        Specify comparison precision. 5 digits (False) or 3 digits (True)\n        after decimal points are compared. If int, then specify the number\n        of digits to compare.\n\n        When comparing two numbers, if the first number has magnitude less\n        than 1e-5, we compare the two numbers directly and check whether\n        they are equivalent within the specified precision. Otherwise, we\n        compare the **ratio** of the second number to the first number and\n        check whether it is equivalent to 1 within the specified precision.\n    "
    if isinstance(left, pd.Index):
        assert_index_equal(left, right, check_exact=False, exact=check_dtype, check_less_precise=check_less_precise, **kwargs)
    elif isinstance(left, pd.Series):
        assert_series_equal(left, right, check_exact=False, check_dtype=check_dtype, check_less_precise=check_less_precise, **kwargs)
    elif isinstance(left, pd.DataFrame):
        assert_frame_equal(left, right, check_exact=False, check_dtype=check_dtype, check_less_precise=check_less_precise, **kwargs)
    else:
        if check_dtype:
            if (is_number(left) and is_number(right)):
                pass
            elif (is_bool(left) and is_bool(right)):
                pass
            else:
                if (isinstance(left, np.ndarray) or isinstance(right, np.ndarray)):
                    obj = 'numpy array'
                else:
                    obj = 'Input'
                assert_class_equal(left, right, obj=obj)
        _testing.assert_almost_equal(left, right, check_dtype=check_dtype, check_less_precise=check_less_precise, **kwargs)