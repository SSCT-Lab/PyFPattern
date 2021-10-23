def assert_index_equal(left: Index, right: Index, exact: Union[(bool, str)]='equiv', check_names: bool=True, check_less_precise: Union[(bool, int)]=False, check_exact: bool=True, check_categorical: bool=True, obj: str='Index') -> None:
    "\n    Check that left and right Index are equal.\n\n    Parameters\n    ----------\n    left : Index\n    right : Index\n    exact : bool or {'equiv'}, default 'equiv'\n        Whether to check the Index class, dtype and inferred_type\n        are identical. If 'equiv', then RangeIndex can be substituted for\n        Int64Index as well.\n    check_names : bool, default True\n        Whether to check the names attribute.\n    check_less_precise : bool or int, default False\n        Specify comparison precision. Only used when check_exact is False.\n        5 digits (False) or 3 digits (True) after decimal points are compared.\n        If int, then specify the digits to compare\n    check_exact : bool, default True\n        Whether to compare number exactly.\n    check_categorical : bool, default True\n        Whether to compare internal Categorical exactly.\n    obj : str, default 'Index'\n        Specify object name being compared, internally used to show appropriate\n        assertion message\n    "
    __tracebackhide__ = True

    def _check_types(l, r, obj='Index'):
        if exact:
            assert_class_equal(l, r, exact=exact, obj=obj)
            if check_categorical:
                assert_attr_equal('dtype', l, r, obj=obj)
            if (l.inferred_type in ('string', 'unicode')):
                assert (r.inferred_type in ('string', 'unicode'))
            else:
                assert_attr_equal('inferred_type', l, r, obj=obj)

    def _get_ilevel_values(index, level):
        unique = index.levels[level]
        labels = index.codes[level]
        filled = take_1d(unique.values, labels, fill_value=unique._na_value)
        values = unique._shallow_copy(filled, name=index.names[level])
        return values
    _check_isinstance(left, right, Index)
    _check_types(left, right, obj=obj)
    if (left.nlevels != right.nlevels):
        msg1 = '{obj} levels are different'.format(obj=obj)
        msg2 = '{nlevels}, {left}'.format(nlevels=left.nlevels, left=left)
        msg3 = '{nlevels}, {right}'.format(nlevels=right.nlevels, right=right)
        raise_assert_detail(obj, msg1, msg2, msg3)
    if (len(left) != len(right)):
        msg1 = '{obj} length are different'.format(obj=obj)
        msg2 = '{length}, {left}'.format(length=len(left), left=left)
        msg3 = '{length}, {right}'.format(length=len(right), right=right)
        raise_assert_detail(obj, msg1, msg2, msg3)
    if (left.nlevels > 1):
        left = cast(MultiIndex, left)
        right = cast(MultiIndex, right)
        for level in range(left.nlevels):
            llevel = _get_ilevel_values(left, level)
            rlevel = _get_ilevel_values(right, level)
            lobj = 'MultiIndex level [{level}]'.format(level=level)
            assert_index_equal(llevel, rlevel, exact=exact, check_names=check_names, check_less_precise=check_less_precise, check_exact=check_exact, obj=lobj)
            _check_types(left.levels[level], right.levels[level], obj=obj)
    if (check_exact and check_categorical):
        if (not left.equals(right)):
            diff = ((np.sum((left.values != right.values).astype(int)) * 100.0) / len(left))
            msg = '{obj} values are different ({pct} %)'.format(obj=obj, pct=np.round(diff, 5))
            raise_assert_detail(obj, msg, left, right)
    else:
        _testing.assert_almost_equal(left.values, right.values, check_less_precise=check_less_precise, check_dtype=exact, obj=obj, lobj=left, robj=right)
    if check_names:
        assert_attr_equal('names', left, right, obj=obj)
    if (isinstance(left, pd.PeriodIndex) or isinstance(right, pd.PeriodIndex)):
        assert_attr_equal('freq', left, right, obj=obj)
    if (isinstance(left, pd.IntervalIndex) or isinstance(right, pd.IntervalIndex)):
        assert_interval_array_equal(left.values, right.values)
    if check_categorical:
        if (is_categorical_dtype(left) or is_categorical_dtype(right)):
            assert_categorical_equal(left.values, right.values, obj='{obj} category'.format(obj=obj))