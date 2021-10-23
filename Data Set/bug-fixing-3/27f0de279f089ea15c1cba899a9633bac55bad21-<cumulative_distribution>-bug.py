def cumulative_distribution(image, nbins=256):
    'Return cumulative distribution function (cdf) for the given image.\n\n    Parameters\n    ----------\n    image : array\n        Image array.\n    nbins : int\n        Number of bins for image histogram.\n\n    Returns\n    -------\n    img_cdf : array\n        Values of cumulative distribution function.\n    bin_centers : array\n        Centers of bins.\n\n    See Also\n    --------\n    histogram\n\n    References\n    ----------\n    .. [1] https://en.wikipedia.org/wiki/Cumulative_distribution_function\n\n    Examples\n    --------\n    >>> from skimage import data, exposure, img_as_float\n    >>> image = img_as_float(data.camera())\n    >>> hi = exposure.histogram(image)\n    >>> cdf = exposure.cumulative_distribution(image)\n    >>> np.alltrue(cdf[0] == np.cumsum(hi[0])/float(image.size))\n    True\n    '
    (hist, bin_centers) = histogram(image, nbins)
    img_cdf = hist.cumsum()
    img_cdf = (img_cdf / float(img_cdf[(- 1)]))
    return (img_cdf, bin_centers)