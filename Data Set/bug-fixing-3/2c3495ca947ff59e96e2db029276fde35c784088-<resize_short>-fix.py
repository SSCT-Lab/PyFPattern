def resize_short(im, size):
    " \n    Resize an image so that the length of shorter edge is size.\n\n    Example usage:\n    \n    .. code-block:: python\n\n        im = load_image('cat.jpg')\n        im = resize_short(im, 256)\n    \n    :param im: the input image with HWC layout.\n    :type im: ndarray\n    :param size: the shorter edge size of image after resizing.\n    :type size: int\n    "
    (h, w) = im.shape[:2]
    (h_new, w_new) = (size, size)
    if (h > w):
        h_new = ((size * h) / w)
    else:
        w_new = ((size * w) / h)
    im = cv2.resize(im, (w_new, h_new), interpolation=cv2.INTER_CUBIC)
    return im