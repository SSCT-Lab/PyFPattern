

def load(f, as_gray=False):
    'Load an image file located in the data directory.\n\n    Parameters\n    ----------\n    f : string\n        File name.\n    as_gray : bool, optional\n        Whether to convert the image to grayscale.\n\n    Returns\n    -------\n    img : ndarray\n        Image loaded from ``skimage.data_dir``.\n\n    Notes\n    -----\n    This functions is deprecated and will be removed in 0.18.\n    '
    warn('This function is deprecated and will be removed in 0.18. Use `skimage.io.load` or `imageio.imread` directly.', stacklevel=2)
    return _load(f, as_gray=as_gray)
