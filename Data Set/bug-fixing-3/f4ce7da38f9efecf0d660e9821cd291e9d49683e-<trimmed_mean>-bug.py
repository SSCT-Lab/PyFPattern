def trimmed_mean(a, limits=(0.1, 0.1), inclusive=(1, 1), relative=True, axis=None):
    ('Returns the trimmed mean of the data along the given axis.\n\n    %s\n\n    ' % trimdoc)
    if ((not isinstance(limits, tuple)) and isinstance(limits, float)):
        limits = (limits, limits)
    if relative:
        return trimr(a, limits=limits, inclusive=inclusive, axis=axis).mean(axis=axis)
    else:
        return trima(a, limits=limits, inclusive=inclusive).mean(axis=axis)