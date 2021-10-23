def assert_interval_array_equal(left, right, exact='equiv', obj='IntervalArray'):
    "Test that two IntervalArrays are equivalent.\n\n    Parameters\n    ----------\n    left, right : IntervalArray\n        The IntervalArrays to compare.\n    exact : bool or {'equiv'}, default 'equiv'\n        Whether to check the Index class, dtype and inferred_type\n        are identical. If 'equiv', then RangeIndex can be substituted for\n        Int64Index as well.\n    obj : str, default 'IntervalArray'\n        Specify object name being compared, internally used to show appropriate\n        assertion message\n    "
    _check_isinstance(left, right, IntervalArray)
    assert_index_equal(left.left, right.left, exact=exact, obj='{obj}.left'.format(obj=obj))
    assert_index_equal(left.right, right.right, exact=exact, obj='{obj}.left'.format(obj=obj))
    assert_attr_equal('closed', left, right, obj=obj)