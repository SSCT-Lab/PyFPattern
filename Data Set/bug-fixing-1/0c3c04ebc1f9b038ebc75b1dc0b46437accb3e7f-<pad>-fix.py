

@array_function_dispatch(_pad_dispatcher, module='numpy')
def pad(array, pad_width, mode='constant', **kwargs):
    "\n    Pads an array.\n\n    Parameters\n    ----------\n    array : array_like of rank N\n        Input array\n    pad_width : {sequence, array_like, int}\n        Number of values padded to the edges of each axis.\n        ((before_1, after_1), ... (before_N, after_N)) unique pad widths\n        for each axis.\n        ((before, after),) yields same before and after pad for each axis.\n        (pad,) or int is a shortcut for before = after = pad width for all\n        axes.\n    mode : str or function, optional\n        One of the following string values or a user supplied function.\n\n        'constant' (default)\n            Pads with a constant value.\n        'edge'\n            Pads with the edge values of array.\n        'linear_ramp'\n            Pads with the linear ramp between end_value and the\n            array edge value.\n        'maximum'\n            Pads with the maximum value of all or part of the\n            vector along each axis.\n        'mean'\n            Pads with the mean value of all or part of the\n            vector along each axis.\n        'median'\n            Pads with the median value of all or part of the\n            vector along each axis.\n        'minimum'\n            Pads with the minimum value of all or part of the\n            vector along each axis.\n        'reflect'\n            Pads with the reflection of the vector mirrored on\n            the first and last values of the vector along each\n            axis.\n        'symmetric'\n            Pads with the reflection of the vector mirrored\n            along the edge of the array.\n        'wrap'\n            Pads with the wrap of the vector along the axis.\n            The first values are used to pad the end and the\n            end values are used to pad the beginning.\n        <function>\n            Padding function, see Notes.\n    stat_length : sequence or int, optional\n        Used in 'maximum', 'mean', 'median', and 'minimum'.  Number of\n        values at edge of each axis used to calculate the statistic value.\n\n        ((before_1, after_1), ... (before_N, after_N)) unique statistic\n        lengths for each axis.\n\n        ((before, after),) yields same before and after statistic lengths\n        for each axis.\n\n        (stat_length,) or int is a shortcut for before = after = statistic\n        length for all axes.\n\n        Default is ``None``, to use the entire axis.\n    constant_values : sequence or scalar, optional\n        Used in 'constant'.  The values to set the padded values for each\n        axis.\n\n        ``((before_1, after_1), ... (before_N, after_N))`` unique pad constants\n        for each axis.\n\n        ``((before, after),)`` yields same before and after constants for each\n        axis.\n\n        ``(constant,)`` or ``constant`` is a shortcut for ``before = after = constant`` for\n        all axes.\n\n        Default is 0.\n    end_values : sequence or scalar, optional\n        Used in 'linear_ramp'.  The values used for the ending value of the\n        linear_ramp and that will form the edge of the padded array.\n\n        ``((before_1, after_1), ... (before_N, after_N))`` unique end values\n        for each axis.\n\n        ``((before, after),)`` yields same before and after end values for each\n        axis.\n\n        ``(constant,)`` or ``constant`` is a shortcut for ``before = after = constant`` for\n        all axes.\n\n        Default is 0.\n    reflect_type : {'even', 'odd'}, optional\n        Used in 'reflect', and 'symmetric'.  The 'even' style is the\n        default with an unaltered reflection around the edge value.  For\n        the 'odd' style, the extended part of the array is created by\n        subtracting the reflected values from two times the edge value.\n\n    Returns\n    -------\n    pad : ndarray\n        Padded array of rank equal to `array` with shape increased\n        according to `pad_width`.\n\n    Notes\n    -----\n    .. versionadded:: 1.7.0\n\n    For an array with rank greater than 1, some of the padding of later\n    axes is calculated from padding of previous axes.  This is easiest to\n    think about with a rank 2 array where the corners of the padded array\n    are calculated by using padded values from the first axis.\n\n    The padding function, if used, should return a rank 1 array equal in\n    length to the vector argument with padded values replaced. It has the\n    following signature::\n\n        padding_func(vector, iaxis_pad_width, iaxis, kwargs)\n\n    where\n\n        vector : ndarray\n            A rank 1 array already padded with zeros.  Padded values are\n            vector[:pad_tuple[0]] and vector[-pad_tuple[1]:].\n        iaxis_pad_width : tuple\n            A 2-tuple of ints, iaxis_pad_width[0] represents the number of\n            values padded at the beginning of vector where\n            iaxis_pad_width[1] represents the number of values padded at\n            the end of vector.\n        iaxis : int\n            The axis currently being calculated.\n        kwargs : dict\n            Any keyword arguments the function requires.\n\n    Examples\n    --------\n    >>> a = [1, 2, 3, 4, 5]\n    >>> np.pad(a, (2,3), 'constant', constant_values=(4, 6))\n    array([4, 4, 1, ..., 6, 6, 6])\n\n    >>> np.pad(a, (2, 3), 'edge')\n    array([1, 1, 1, ..., 5, 5, 5])\n\n    >>> np.pad(a, (2, 3), 'linear_ramp', end_values=(5, -4))\n    array([ 5,  3,  1,  2,  3,  4,  5,  2, -1, -4])\n\n    >>> np.pad(a, (2,), 'maximum')\n    array([5, 5, 1, 2, 3, 4, 5, 5, 5])\n\n    >>> np.pad(a, (2,), 'mean')\n    array([3, 3, 1, 2, 3, 4, 5, 3, 3])\n\n    >>> np.pad(a, (2,), 'median')\n    array([3, 3, 1, 2, 3, 4, 5, 3, 3])\n\n    >>> a = [[1, 2], [3, 4]]\n    >>> np.pad(a, ((3, 2), (2, 3)), 'minimum')\n    array([[1, 1, 1, 2, 1, 1, 1],\n           [1, 1, 1, 2, 1, 1, 1],\n           [1, 1, 1, 2, 1, 1, 1],\n           [1, 1, 1, 2, 1, 1, 1],\n           [3, 3, 3, 4, 3, 3, 3],\n           [1, 1, 1, 2, 1, 1, 1],\n           [1, 1, 1, 2, 1, 1, 1]])\n\n    >>> a = [1, 2, 3, 4, 5]\n    >>> np.pad(a, (2, 3), 'reflect')\n    array([3, 2, 1, 2, 3, 4, 5, 4, 3, 2])\n\n    >>> np.pad(a, (2, 3), 'reflect', reflect_type='odd')\n    array([-1,  0,  1,  2,  3,  4,  5,  6,  7,  8])\n\n    >>> np.pad(a, (2, 3), 'symmetric')\n    array([2, 1, 1, 2, 3, 4, 5, 5, 4, 3])\n\n    >>> np.pad(a, (2, 3), 'symmetric', reflect_type='odd')\n    array([0, 1, 1, 2, 3, 4, 5, 5, 6, 7])\n\n    >>> np.pad(a, (2, 3), 'wrap')\n    array([4, 5, 1, 2, 3, 4, 5, 1, 2, 3])\n\n    >>> def pad_with(vector, pad_width, iaxis, kwargs):\n    ...     pad_value = kwargs.get('padder', 10)\n    ...     vector[:pad_width[0]] = pad_value\n    ...     vector[-pad_width[1]:] = pad_value\n    ...     return vector\n    >>> a = np.arange(6)\n    >>> a = a.reshape((2, 3))\n    >>> np.pad(a, 2, pad_with)\n    array([[10, 10, 10, 10, 10, 10, 10],\n           [10, 10, 10, 10, 10, 10, 10],\n           [10, 10,  0,  1,  2, 10, 10],\n           [10, 10,  3,  4,  5, 10, 10],\n           [10, 10, 10, 10, 10, 10, 10],\n           [10, 10, 10, 10, 10, 10, 10]])\n    >>> np.pad(a, 2, pad_with, padder=100)\n    array([[100, 100, 100, 100, 100, 100, 100],\n           [100, 100, 100, 100, 100, 100, 100],\n           [100, 100,   0,   1,   2, 100, 100],\n           [100, 100,   3,   4,   5, 100, 100],\n           [100, 100, 100, 100, 100, 100, 100],\n           [100, 100, 100, 100, 100, 100, 100]])\n    "
    if (not (np.asarray(pad_width).dtype.kind == 'i')):
        raise TypeError('`pad_width` must be of integral type.')
    narray = np.array(array)
    pad_width = _as_pairs(pad_width, narray.ndim, as_index=True)
    allowedkwargs = {
        'constant': ['constant_values'],
        'edge': [],
        'linear_ramp': ['end_values'],
        'maximum': ['stat_length'],
        'mean': ['stat_length'],
        'median': ['stat_length'],
        'minimum': ['stat_length'],
        'reflect': ['reflect_type'],
        'symmetric': ['reflect_type'],
        'wrap': [],
    }
    kwdefaults = {
        'stat_length': None,
        'constant_values': 0,
        'end_values': 0,
        'reflect_type': 'even',
    }
    if isinstance(mode, np.compat.basestring):
        for key in kwargs:
            if (key not in allowedkwargs[mode]):
                raise ValueError(('%s keyword not in allowed keywords %s' % (key, allowedkwargs[mode])))
        for kw in allowedkwargs[mode]:
            kwargs.setdefault(kw, kwdefaults[kw])
        for i in kwargs:
            if (i == 'stat_length'):
                kwargs[i] = _as_pairs(kwargs[i], narray.ndim, as_index=True)
            if (i in ['end_values', 'constant_values']):
                kwargs[i] = _as_pairs(kwargs[i], narray.ndim)
    else:
        function = mode
        rank = list(range(narray.ndim))
        total_dim_increase = [np.sum(pad_width[i]) for i in rank]
        offset_slices = tuple((slice(pad_width[i][0], (pad_width[i][0] + narray.shape[i])) for i in rank))
        new_shape = (np.array(narray.shape) + total_dim_increase)
        newmat = np.zeros(new_shape, narray.dtype)
        newmat[offset_slices] = narray
        for iaxis in rank:
            np.apply_along_axis(function, iaxis, newmat, pad_width[iaxis], iaxis, kwargs)
        return newmat
    newmat = narray.copy()
    if (mode == 'constant'):
        for (axis, ((pad_before, pad_after), (before_val, after_val))) in enumerate(zip(pad_width, kwargs['constant_values'])):
            newmat = _prepend_const(newmat, pad_before, before_val, axis)
            newmat = _append_const(newmat, pad_after, after_val, axis)
    elif (mode == 'edge'):
        for (axis, (pad_before, pad_after)) in enumerate(pad_width):
            newmat = _prepend_edge(newmat, pad_before, axis)
            newmat = _append_edge(newmat, pad_after, axis)
    elif (mode == 'linear_ramp'):
        for (axis, ((pad_before, pad_after), (before_val, after_val))) in enumerate(zip(pad_width, kwargs['end_values'])):
            newmat = _prepend_ramp(newmat, pad_before, before_val, axis)
            newmat = _append_ramp(newmat, pad_after, after_val, axis)
    elif (mode == 'maximum'):
        for (axis, ((pad_before, pad_after), (chunk_before, chunk_after))) in enumerate(zip(pad_width, kwargs['stat_length'])):
            newmat = _prepend_max(newmat, pad_before, chunk_before, axis)
            newmat = _append_max(newmat, pad_after, chunk_after, axis)
    elif (mode == 'mean'):
        for (axis, ((pad_before, pad_after), (chunk_before, chunk_after))) in enumerate(zip(pad_width, kwargs['stat_length'])):
            newmat = _prepend_mean(newmat, pad_before, chunk_before, axis)
            newmat = _append_mean(newmat, pad_after, chunk_after, axis)
    elif (mode == 'median'):
        for (axis, ((pad_before, pad_after), (chunk_before, chunk_after))) in enumerate(zip(pad_width, kwargs['stat_length'])):
            newmat = _prepend_med(newmat, pad_before, chunk_before, axis)
            newmat = _append_med(newmat, pad_after, chunk_after, axis)
    elif (mode == 'minimum'):
        for (axis, ((pad_before, pad_after), (chunk_before, chunk_after))) in enumerate(zip(pad_width, kwargs['stat_length'])):
            newmat = _prepend_min(newmat, pad_before, chunk_before, axis)
            newmat = _append_min(newmat, pad_after, chunk_after, axis)
    elif (mode == 'reflect'):
        for (axis, (pad_before, pad_after)) in enumerate(pad_width):
            if (narray.shape[axis] == 0):
                if ((pad_before > 0) or (pad_after > 0)):
                    raise ValueError("There aren't any elements to reflect in axis {} of `array`".format(axis))
                continue
            if (((pad_before > 0) or (pad_after > 0)) and (newmat.shape[axis] == 1)):
                newmat = _prepend_edge(newmat, pad_before, axis)
                newmat = _append_edge(newmat, pad_after, axis)
                continue
            method = kwargs['reflect_type']
            safe_pad = (newmat.shape[axis] - 1)
            while ((pad_before > safe_pad) or (pad_after > safe_pad)):
                pad_iter_b = min(safe_pad, (safe_pad * (pad_before // safe_pad)))
                pad_iter_a = min(safe_pad, (safe_pad * (pad_after // safe_pad)))
                newmat = _pad_ref(newmat, (pad_iter_b, pad_iter_a), method, axis)
                pad_before -= pad_iter_b
                pad_after -= pad_iter_a
                safe_pad += (pad_iter_b + pad_iter_a)
            newmat = _pad_ref(newmat, (pad_before, pad_after), method, axis)
    elif (mode == 'symmetric'):
        for (axis, (pad_before, pad_after)) in enumerate(pad_width):
            method = kwargs['reflect_type']
            safe_pad = newmat.shape[axis]
            while ((pad_before > safe_pad) or (pad_after > safe_pad)):
                pad_iter_b = min(safe_pad, (safe_pad * (pad_before // safe_pad)))
                pad_iter_a = min(safe_pad, (safe_pad * (pad_after // safe_pad)))
                newmat = _pad_sym(newmat, (pad_iter_b, pad_iter_a), method, axis)
                pad_before -= pad_iter_b
                pad_after -= pad_iter_a
                safe_pad += (pad_iter_b + pad_iter_a)
            newmat = _pad_sym(newmat, (pad_before, pad_after), method, axis)
    elif (mode == 'wrap'):
        for (axis, (pad_before, pad_after)) in enumerate(pad_width):
            safe_pad = newmat.shape[axis]
            while ((pad_before > safe_pad) or (pad_after > safe_pad)):
                pad_iter_b = min(safe_pad, (safe_pad * (pad_before // safe_pad)))
                pad_iter_a = min(safe_pad, (safe_pad * (pad_after // safe_pad)))
                newmat = _pad_wrap(newmat, (pad_iter_b, pad_iter_a), axis)
                pad_before -= pad_iter_b
                pad_after -= pad_iter_a
                safe_pad += (pad_iter_b + pad_iter_a)
            newmat = _pad_wrap(newmat, (pad_before, pad_after), axis)
    return newmat
