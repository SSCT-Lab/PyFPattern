@default_selem
def black_tophat(image, selem=None, out=None):
    "Return black top hat of an image.\n\n    The black top hat of an image is defined as its morphological closing minus\n    the original image. This operation returns the dark spots of the image that\n    are smaller than the structuring element. Note that dark spots in the\n    original image are bright spots after the black top hat.\n\n    Parameters\n    ----------\n    image : ndarray\n        Image array.\n    selem : ndarray, optional\n        The neighborhood expressed as a 2-D array of 1's and 0's.\n        If None, use cross-shaped structuring element (connectivity=1).\n    out : ndarray, optional\n        The array to store the result of the morphology. If None\n        is passed, a new array will be allocated.\n\n    Returns\n    -------\n    opening : array, same shape and type as `image`\n       The result of the black top filter.\n\n    Examples\n    --------\n    >>> # Change dark peak to bright peak and subtract background\n    >>> import numpy as np\n    >>> from skimage.morphology import square\n    >>> dark_on_grey = np.array([[7, 6, 6, 6, 7],\n    ...                          [6, 5, 4, 5, 6],\n    ...                          [6, 4, 0, 4, 6],\n    ...                          [6, 5, 4, 5, 6],\n    ...                          [7, 6, 6, 6, 7]], dtype=np.uint8)\n    >>> black_tophat(dark_on_grey, square(3))\n    array([[0, 0, 0, 0, 0],\n           [0, 0, 1, 0, 0],\n           [0, 1, 5, 1, 0],\n           [0, 0, 1, 0, 0],\n           [0, 0, 0, 0, 0]], dtype=uint8)\n\n    "
    if (out is image):
        original = image.copy()
    else:
        original = image
    out = closing(image, selem, out=out)
    out -= original
    return out