def load_image_bytes(bytes, is_color=True):
    "\n    Load an color or gray image from bytes array.\n\n    Example usage:\n\n    .. code-block:: python\n\n        with open('cat.jpg') as f:\n            im = load_image_bytes(f.read())\n\n    :param bytes: the input image bytes array.\n    :type bytes: str\n    :param is_color: If set is_color True, it will load and\n                     return a color image. Otherwise, it will\n                     load and return a gray image.\n    :type is_color: bool\n    "
    assert (_check_cv2() is True)
    flag = (1 if is_color else 0)
    file_bytes = np.asarray(bytearray(bytes), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, flag)
    return img