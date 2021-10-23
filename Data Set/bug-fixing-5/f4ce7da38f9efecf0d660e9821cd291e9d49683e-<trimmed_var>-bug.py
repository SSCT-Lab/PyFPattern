def trimmed_var(a, limits=(0.1, 0.1), inclusive=(1, 1), relative=True, axis=None, ddof=0):
    ('Returns the trimmed variance of the data along the given axis.\n\n    %s\n    ddof : {0,integer}, optional\n        Means Delta Degrees of Freedom. The denominator used during computations\n        is (n-ddof). DDOF=0 corresponds to a biased estimate, DDOF=1 to an un-\n        biased estimate of the variance.\n\n    ' % trimdoc)
    if ((not isinstance(limits, tuple)) and isinstance(limits, float)):
        limits = (limits, limits)
    if relative:
        out = trimr(a, limits=limits, inclusive=inclusive, axis=axis)
    else:
        out = trima(a, limits=limits, inclusive=inclusive)
    return out.var(axis=axis, ddof=ddof)