

def denoise_bilateral(image, win_size=None, sigma_color=None, sigma_spatial=1, bins=10000, mode='constant', cval=0, multichannel=True, sigma_range=None):
    "Denoise image using bilateral filter.\n\n    This is an edge-preserving and noise reducing denoising filter. It averages\n    pixels based on their spatial closeness and radiometric similarity.\n\n    Spatial closeness is measured by the gaussian function of the euclidian\n    distance between two pixels and a certain standard deviation\n    (`sigma_spatial`).\n\n    Radiometric similarity is measured by the gaussian function of the euclidian\n    distance between two color values and a certain standard deviation\n    (`sigma_color`).\n\n    Parameters\n    ----------\n    image : ndarray, shape (M, N[, 3])\n        Input image, 2D grayscale or RGB.\n    win_size : int\n        Window size for filtering.\n        If win_size is not specified, it is calculated as max(5, 2*ceil(3*sigma_spatial)+1)\n    sigma_color : float\n        Standard deviation for grayvalue/color distance (radiometric\n        similarity). A larger value results in averaging of pixels with larger\n        radiometric differences. Note, that the image will be converted using\n        the `img_as_float` function and thus the standard deviation is in\n        respect to the range ``[0, 1]``. If the value is ``None`` the standard\n        deviation of the ``image`` will be used.\n    sigma_spatial : float\n        Standard deviation for range distance. A larger value results in\n        averaging of pixels with larger spatial differences.\n    bins : int\n        Number of discrete values for gaussian weights of color filtering.\n        A larger value results in improved accuracy.\n    mode : {'constant', 'edge', 'symmetric', 'reflect', 'wrap'}\n        How to handle values outside the image borders. See\n        `numpy.pad` for detail.\n    cval : string\n        Used in conjunction with mode 'constant', the value outside\n        the image boundaries.\n    multichannel : bool\n        Whether the last axis of the image is to be interpreted as multiple\n        channels or another spatial dimension.\n\n    Returns\n    -------\n    denoised : ndarray\n        Denoised image.\n\n    References\n    ----------\n    .. [1] http://users.soe.ucsc.edu/~manduchi/Papers/ICCV98.pdf\n\n    Examples\n    --------\n    >>> from skimage import data, img_as_float\n    >>> astro = img_as_float(data.astronaut())\n    >>> astro = astro[220:300, 220:320]\n    >>> noisy = astro + 0.6 * astro.std() * np.random.random(astro.shape)\n    >>> noisy = np.clip(noisy, 0, 1)\n    >>> denoised = denoise_bilateral(noisy, sigma_color=0.05, sigma_spatial=15)\n    "
    if multichannel:
        if (image.ndim != 3):
            if (image.ndim == 2):
                raise ValueError('Use ``multichannel=False`` for 2D grayscale images. The last axis of the input image must be multiple color channels not another spatial dimension.')
            else:
                raise ValueError('Bilateral filter is only implemented for 2D grayscale images (image.ndim == 2) and 2D multichannel (image.ndim == 3) images, but the input image has {0} dimensions. '.format(image.ndim))
        elif (image.shape[2] not in (3, 4)):
            if (image.shape[2] > 4):
                warnings.warn('The last axis of the input image is interpreted as channels. Input image with shape {0} has {1} channels in last axis. ``denoise_bilateral`` is implemented for 2D grayscale and color images only.'.format(image.shape, image.shape[2]))
            else:
                msg = 'Input image must be grayscale, RGB, or RGBA; but has shape {0}.'
                warnings.warn(msg.format(image.shape))
    elif (image.ndim > 2):
        raise ValueError('Bilateral filter is not implemented for grayscale images of 3 or more dimensions, but input image has {0} dimension. Use ``multichannel=True`` for 2-D RGB images.'.format(image.shape))
    if (sigma_range is not None):
        warn('`sigma_range` has been deprecated in favor of `sigma_color`. The `sigma_range` keyword argument will be removed in v0.14', skimage_deprecation)
        sigma_color = sigma_range
    if (win_size is None):
        win_size = max(5, ((2 * int(ceil((3 * sigma_spatial)))) + 1))
    mode = _mode_deprecations(mode)
    return _denoise_bilateral(image, win_size, sigma_color, sigma_spatial, bins, mode, cval)
