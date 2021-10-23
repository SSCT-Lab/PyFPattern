def simple_transform(im, resize_size, crop_size, is_train, is_color=True, mean=None):
    '\n    Simply data argumentation for training. These operations include\n    resizing, croping and flipping.\n\n    Example usage:\n\n    .. code-block:: python\n\n        im = simple_transform(im, 256, 224, True)\n\n    :param im: The input image with HWC layout.\n    :type im: ndarray\n    :param resize_size: The shorter edge length of the resized image.\n    :type resize_size: int\n    :param crop_size: The cropping size.\n    :type crop_size: int\n    :param is_train: Whether it is training or not.\n    :type is_train: bool\n    :param is_color: whether the image is color or not.\n    :type is_color: bool\n    :param mean: the mean values, which can be element-wise mean values or\n                 mean values per channel.\n    :type mean: numpy array | list\n    '
    im = resize_short(im, resize_size)
    if is_train:
        im = random_crop(im, crop_size, is_color=is_color)
        if (np.random.randint(2) == 0):
            im = left_right_flip(im, is_color)
    else:
        im = center_crop(im, crop_size, is_color)
        im = center_crop(im, crop_size, is_color=is_color)
    if (len(im.shape) == 3):
        im = to_chw(im)
    im = im.astype('float32')
    if (mean is not None):
        mean = np.array(mean, dtype=np.float32)
        if ((mean.ndim == 1) and is_color):
            mean = mean[:, np.newaxis, np.newaxis]
        elif (mean.ndim == 1):
            mean = mean
        else:
            assert (len(mean.shape) == len(im))
        im -= mean
    return im