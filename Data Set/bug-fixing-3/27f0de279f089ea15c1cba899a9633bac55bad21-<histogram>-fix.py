def histogram(image, nbins=256):
    'Return histogram of image.\n\n    Unlike `numpy.histogram`, this function returns the centers of bins and\n    does not rebin integer arrays. For integer arrays, each integer value has\n    its own bin, which improves speed and intensity-resolution.\n\n    The histogram is computed on the flattened image: for color images, the\n    function should be used separately on each channel to obtain a histogram\n    for each color channel.\n\n    Parameters\n    ----------\n    image : array\n        Input image.\n    nbins : int, optional\n        Number of bins used to calculate histogram. This value is ignored for\n        integer arrays.\n\n    Returns\n    -------\n    hist : array\n        The values of the histogram.\n    bin_centers : array\n        The values at the center of the bins.\n\n    See Also\n    --------\n    cumulative_distribution\n\n    Examples\n    --------\n    >>> from skimage import data, exposure, img_as_float\n    >>> image = img_as_float(data.camera())\n    >>> np.histogram(image, bins=2)\n    (array([107432, 154712]), array([ 0. ,  0.5,  1. ]))\n    >>> exposure.histogram(image, nbins=2)\n    (array([107432, 154712]), array([ 0.25,  0.75]))\n    '
    sh = image.shape
    if ((len(sh) == 3) and (sh[(- 1)] < 4)):
        warn('This might be a color image. The histogram will be computed on the flattened image. You can instead apply this function to each color channel.')
    if np.issubdtype(image.dtype, np.integer):
        offset = 0
        image_min = np.min(image)
        if (image_min < 0):
            offset = image_min
            image_range = (np.max(image).astype(np.int64) - image_min)
            offset_dtype = np.promote_types(np.min_scalar_type(image_range), np.min_scalar_type(image_min))
            if (image.dtype != offset_dtype):
                image = image.astype(offset_dtype)
            image = (image - offset)
        hist = np.bincount(image.ravel())
        bin_centers = (np.arange(len(hist)) + offset)
        idx = np.nonzero(hist)[0][0]
        return (hist[idx:], bin_centers[idx:])
    else:
        (hist, bin_edges) = np.histogram(image.flat, bins=nbins)
        bin_centers = ((bin_edges[:(- 1)] + bin_edges[1:]) / 2.0)
        return (hist, bin_centers)