

def _cython_operation(self, kind, values, how, axis, min_count=(- 1), **kwargs):
    assert (kind in ['transform', 'aggregate'])
    orig_values = values
    if (is_categorical_dtype(values) or is_sparse(values)):
        raise NotImplementedError('{} are not support in cython ops'.format(values.dtype))
    elif is_datetime64_any_dtype(values):
        if (how in ['add', 'prod', 'cumsum', 'cumprod']):
            raise NotImplementedError('datetime64 type does not support {} operations'.format(how))
    elif is_timedelta64_dtype(values):
        if (how in ['prod', 'cumprod']):
            raise NotImplementedError('timedelta64 type does not support {} operations'.format(how))
    if is_datetime64tz_dtype(values.dtype):
        values = values.view('M8[ns]')
    is_datetimelike = needs_i8_conversion(values.dtype)
    is_numeric = is_numeric_dtype(values.dtype)
    if is_datetimelike:
        values = values.view('int64')
        is_numeric = True
    elif is_bool_dtype(values.dtype):
        values = ensure_float64(values)
    elif is_integer_dtype(values):
        if (values == iNaT).any():
            values = ensure_float64(values)
        else:
            values = ensure_int_or_float(values)
    elif (is_numeric and (not is_complex_dtype(values))):
        values = ensure_float64(values)
    else:
        values = values.astype(object)
    arity = self._cython_arity.get(how, 1)
    vdim = values.ndim
    swapped = False
    if (vdim == 1):
        values = values[:, None]
        out_shape = (self.ngroups, arity)
    else:
        if (axis > 0):
            swapped = True
            assert (axis == 1), axis
            values = values.T
        if (arity > 1):
            raise NotImplementedError("arity of more than 1 is not supported for the 'how' argument")
        out_shape = ((self.ngroups,) + values.shape[1:])
    try:
        func = self._get_cython_function(kind, how, values, is_numeric)
    except NotImplementedError:
        if is_numeric:
            values = ensure_float64(values)
            func = self._get_cython_function(kind, how, values, is_numeric)
        else:
            raise
    if (how == 'rank'):
        out_dtype = 'float'
    elif is_numeric:
        out_dtype = '{kind}{itemsize}'.format(kind=values.dtype.kind, itemsize=values.dtype.itemsize)
    else:
        out_dtype = 'object'
    (labels, _, _) = self.group_info
    if (kind == 'aggregate'):
        result = _maybe_fill(np.empty(out_shape, dtype=out_dtype), fill_value=np.nan)
        counts = np.zeros(self.ngroups, dtype=np.int64)
        result = self._aggregate(result, counts, values, labels, func, is_numeric, is_datetimelike, min_count)
    elif (kind == 'transform'):
        result = _maybe_fill(np.empty_like(values, dtype=out_dtype), fill_value=np.nan)
        result = self._transform(result, values, labels, func, is_numeric, is_datetimelike, **kwargs)
    if (is_integer_dtype(result) and (not is_datetimelike)):
        mask = (result == iNaT)
        if mask.any():
            result = result.astype('float64')
            result[mask] = np.nan
    if ((kind == 'aggregate') and self._filter_empty_groups and (not counts.all())):
        assert (result.ndim != 2)
        result = result[(counts > 0)]
    if ((vdim == 1) and (arity == 1)):
        result = result[:, 0]
    if (how in self._name_functions):
        names = self._name_functions[how]()
    else:
        names = None
    if swapped:
        result = result.swapaxes(0, axis)
    if is_datetime64tz_dtype(orig_values.dtype):
        result = type(orig_values)(result.astype(np.int64), dtype=orig_values.dtype)
    elif (is_datetimelike and (kind == 'aggregate')):
        result = result.astype(orig_values.dtype)
    return (result, names)
