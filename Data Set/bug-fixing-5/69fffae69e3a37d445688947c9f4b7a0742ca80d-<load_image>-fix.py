def load_image(file, is_color=True):
    "\n    Load an color or gray image from the file path.\n\n    Example usage:\n\n    .. code-block:: python\n\n        im = load_image('cat.jpg')\n\n    :param file: the input image path.\n    :type file: string\n    :param is_color: If set is_color True, it will load and\n                     return a color image. Otherwise, it will\n                     load and return a gray image.\n    :type is_color: bool\n    "
    assert (_check_cv2() is True)
    flag = (1 if is_color else 0)
    im = cv2.imread(file, flag)
    return im