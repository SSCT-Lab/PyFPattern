

def winsorize(a, limits=None, inclusive=(True, True), inplace=False, axis=None):
    'Returns a Winsorized version of the input array.\n\n    The (limits[0])th lowest values are set to the (limits[0])th percentile,\n    and the (limits[1])th highest values are set to the (1 - limits[1])th\n    percentile.\n    Masked values are skipped.\n\n\n    Parameters\n    ----------\n    a : sequence\n        Input array.\n    limits : {None, tuple of float}, optional\n        Tuple of the percentages to cut on each side of the array, with respect\n        to the number of unmasked data, as floats between 0. and 1.\n        Noting n the number of unmasked data before trimming, the\n        (n*limits[0])th smallest data and the (n*limits[1])th largest data are\n        masked, and the total number of unmasked data after trimming\n        is n*(1.-sum(limits)) The value of one limit can be set to None to\n        indicate an open interval.\n    inclusive : {(True, True) tuple}, optional\n        Tuple indicating whether the number of data being masked on each side\n        should be truncated (True) or rounded (False).\n    inplace : {False, True}, optional\n        Whether to winsorize in place (True) or to use a copy (False)\n    axis : {None, int}, optional\n        Axis along which to trim. If None, the whole array is trimmed, but its\n        shape is maintained.\n\n    Notes\n    -----\n    This function is applied to reduce the effect of possibly spurious outliers\n    by limiting the extreme values.\n\n    '

    def _winsorize1D(a, low_limit, up_limit, low_include, up_include):
        n = a.count()
        idx = a.argsort()
        if low_limit:
            if low_include:
                lowidx = int((low_limit * n))
            else:
                lowidx = np.round((low_limit * n)).astype(int)
            a[idx[:lowidx]] = a[idx[lowidx]]
        if (up_limit is not None):
            if up_include:
                upidx = (n - int((n * up_limit)))
            else:
                upidx = (n - np.round((n * up_limit)).astype(int))
            a[idx[upidx:]] = a[idx[(upidx - 1)]]
        return a
    a = ma.array(a, copy=np.logical_not(inplace))
    if (limits is None):
        return a
    if ((not isinstance(limits, tuple)) and isinstance(limits, float)):
        limits = (limits, limits)
    (lolim, uplim) = limits
    errmsg = 'The proportion to cut from the %s should be between 0. and 1.'
    if (lolim is not None):
        if ((lolim > 1.0) or (lolim < 0)):
            raise ValueError(((errmsg % 'beginning') + ('(got %s)' % lolim)))
    if (uplim is not None):
        if ((uplim > 1.0) or (uplim < 0)):
            raise ValueError(((errmsg % 'end') + ('(got %s)' % uplim)))
    (loinc, upinc) = inclusive
    if (axis is None):
        shp = a.shape
        return _winsorize1D(a.ravel(), lolim, uplim, loinc, upinc).reshape(shp)
    else:
        return ma.apply_along_axis(_winsorize1D, axis, a, lolim, uplim, loinc, upinc)
