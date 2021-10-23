

def resize_long(src, size, interp=2):
    'Resizes longer edge to size.\n    Note: `resize_long` uses OpenCV (not the CV2 Python library).\n    MXNet must have been built with OpenCV for `resize_long` to work.\n    Resizes the original image by setting the longer edge to size\n    and setting the shorter edge accordingly. This will ensure the new image will\n    fit into the `size` specified.\n    Resizing function is called from OpenCV.\n\n    Parameters\n    ----------\n    src : NDArray\n        The original image.\n    size : int\n        The length to be set for the shorter edge.\n    interp : int, optional, default=2\n        Interpolation method used for resizing the image.\n        Possible values:\n        0: Nearest Neighbors Interpolation.\n        1: Bilinear interpolation.\n        2: Area-based (resampling using pixel area relation). It may be a\n        preferred method for image decimation, as it gives moire-free\n        results. But when the image is zoomed, it is similar to the Nearest\n        Neighbors method. (used by default).\n        3: Bicubic interpolation over 4x4 pixel neighborhood.\n        4: Lanczos interpolation over 8x8 pixel neighborhood.\n        9: Cubic for enlarge, area for shrink, bilinear for others\n        10: Random select from interpolation method mentioned above.\n        Note:\n        When shrinking an image, it will generally look best with AREA-based\n        interpolation, whereas, when enlarging an image, it will generally look best\n        with Bicubic (slow) or Bilinear (faster but still looks OK).\n        More details can be found in the documentation of OpenCV, please refer to\n        http://docs.opencv.org/master/da/d54/group__imgproc__transform.html.\n    Returns\n    -------\n    NDArray\n        An \'NDArray\' containing the resized image.\n    Example\n    -------\n    >>> with open("flower.jpeg", \'rb\') as fp:\n    ...     str_image = fp.read()\n    ...\n    >>> image = mx.img.imdecode(str_image)\n    >>> image\n    <NDArray 2321x3482x3 @cpu(0)>\n    >>> size = 640\n    >>> new_image = mx.img.resize_long(image, size)\n    >>> new_image\n    <NDArray 386x640x3 @cpu(0)>\n    '
    from mxnet.image.image import _get_interp_method as get_interp
    (h, w, _) = src.shape
    if (h > w):
        (new_h, new_w) = (size, ((size * w) // h))
    else:
        (new_h, new_w) = (((size * h) // w), size)
    return imresize(src, new_w, new_h, interp=get_interp(interp, (h, w, new_h, new_w)))