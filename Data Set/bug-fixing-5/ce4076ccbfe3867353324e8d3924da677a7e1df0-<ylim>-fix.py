def ylim(*args, **kwargs):
    '\n    Get or set the y-limits of the current axes.\n\n    Call signatures::\n\n        bottom, top = ylim()  # return the current ylim\n        ylim((bottom, top))   # set the ylim to bottom, top\n        ylim(bottom, top)     # set the ylim to bottom, top\n\n    If you do not specify args, you can alternatively pass *bottom* or\n    *top* as kwargs, i.e.::\n\n        ylim(top=3)  # adjust the top leaving bottom unchanged\n        ylim(bottom=1)  # adjust the bottom leaving top unchanged\n\n    Setting limits turns autoscaling off for the y-axis.\n\n    Returns\n    -------\n    bottom, top\n        A tuple of the new y-axis limits.\n\n    Notes\n    -----\n    Calling this function with no arguments (e.g. ``ylim()``) is the pyplot\n    equivalent of calling `~.Axes.get_ylim` on the current axes.\n    Calling this function with arguments is the pyplot equivalent of calling\n    `~.Axes.set_ylim` on the current axes. All arguments are passed though.\n    '
    ax = gca()
    if ((not args) and (not kwargs)):
        return ax.get_ylim()
    ret = ax.set_ylim(*args, **kwargs)
    return ret