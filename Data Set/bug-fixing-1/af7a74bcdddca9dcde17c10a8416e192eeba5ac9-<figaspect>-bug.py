

def figaspect(arg):
    '\n    Calculate the width and height for a figure with a specified aspect ratio.\n\n    While the height is taken from :rc:`figure.figsize`, the width is\n    adjusted to match the desired aspect ratio. Additionally, it is ensured\n    that the width is in the range [4., 16.] and the height is in the range\n    [2., 16.]. If necessary, the default height is adjusted to ensure this.\n\n    Parameters\n    ----------\n    arg : scalar or 2d array\n        If a scalar, this defines the aspect ratio (i.e. the ratio height /\n        width).\n        In case of an array the aspect ratio is number of rows / number of\n        columns, so that the array could be fitted in the figure undistorted.\n\n    Returns\n    -------\n    width, height\n        The figure size in inches.\n\n    Notes\n    -----\n    If you want to create an axes within the figure, that still presevers the\n    aspect ratio, be sure to create it with equal width and height. See\n    examples below.\n\n    Thanks to Fernando Perez for this function.\n\n    Examples\n    --------\n    Make a figure twice as tall as it is wide::\n\n        w, h = figaspect(2.)\n        fig = Figure(figsize=(w, h))\n        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])\n        ax.imshow(A, **kwargs)\n\n    Make a figure with the proper aspect for an array::\n\n        A = rand(5,3)\n        w, h = figaspect(A)\n        fig = Figure(figsize=(w, h))\n        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])\n        ax.imshow(A, **kwargs)\n    '
    isarray = (hasattr(arg, 'shape') and (not np.isscalar(arg)))
    figsize_min = np.array((4.0, 2.0))
    figsize_max = np.array((16.0, 16.0))
    if isarray:
        (nr, nc) = arg.shape[:2]
        arr_ratio = (nr / nc)
    else:
        arr_ratio = arg
    fig_height = rcParams['figure.figsize'][1]
    newsize = np.array(((fig_height / arr_ratio), fig_height))
    newsize /= min(1.0, *(newsize / figsize_min))
    newsize /= max(1.0, *(newsize / figsize_max))
    newsize = np.clip(newsize, figsize_min, figsize_max)
    return newsize
