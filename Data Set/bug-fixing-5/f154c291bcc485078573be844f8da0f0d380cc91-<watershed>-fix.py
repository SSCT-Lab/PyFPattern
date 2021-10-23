def watershed(image, markers, connectivity=1, offset=None, mask=None, compactness=0, watershed_line=False):
    'Find watershed basins in `image` flooded from given `markers`.\n\n    Parameters\n    ----------\n    image: ndarray (2-D, 3-D, ...) of integers\n        Data array where the lowest value points are labeled first.\n    markers: int, or ndarray of int, same shape as `image`\n        The desired number of markers, or an array marking the basins with the\n        values to be assigned in the label matrix. Zero means not a marker.\n    connectivity: ndarray, optional\n        An array with the same number of dimensions as `image` whose\n        non-zero elements indicate neighbors for connection.\n        Following the scipy convention, default is a one-connected array of\n        the dimension of the image.\n    offset: array_like of shape image.ndim, optional\n        offset of the connectivity (one offset per dimension)\n    mask: ndarray of bools or 0s and 1s, optional\n        Array of same shape as `image`. Only points at which mask == True\n        will be labeled.\n    compactness : float, optional\n        Use compact watershed [3]_ with given compactness parameter.\n        Higher values result in more regularly-shaped watershed basins.\n    watershed_line : bool, optional\n        If watershed_line is True, a one-pixel wide line separates the regions\n        obtained by the watershed algorithm. The line has the label 0.\n\n    Returns\n    -------\n    out: ndarray\n        A labeled matrix of the same type and shape as markers\n\n    See also\n    --------\n    skimage.segmentation.random_walker: random walker segmentation\n        A segmentation algorithm based on anisotropic diffusion, usually\n        slower than the watershed but with good results on noisy data and\n        boundaries with holes.\n\n    Notes\n    -----\n    This function implements a watershed algorithm [1]_ [2]_ that apportions\n    pixels into marked basins. The algorithm uses a priority queue to hold\n    the pixels with the metric for the priority queue being pixel value, then\n    the time of entry into the queue - this settles ties in favor of the\n    closest marker.\n\n    Some ideas taken from\n    Soille, "Automated Basin Delineation from Digital Elevation Models Using\n    Mathematical Morphology", Signal Processing 20 (1990) 171-182\n\n    The most important insight in the paper is that entry time onto the queue\n    solves two problems: a pixel should be assigned to the neighbor with the\n    largest gradient or, if there is no gradient, pixels on a plateau should\n    be split between markers on opposite sides.\n\n    This implementation converts all arguments to specific, lowest common\n    denominator types, then passes these to a C algorithm.\n\n    Markers can be determined manually, or automatically using for example\n    the local minima of the gradient of the image, or the local maxima of the\n    distance function to the background for separating overlapping objects\n    (see example).\n\n    References\n    ----------\n    .. [1] http://en.wikipedia.org/wiki/Watershed_%28image_processing%29\n\n    .. [2] http://cmm.ensmp.fr/~beucher/wtshed.html\n\n    .. [3] Peer Neubert & Peter Protzel (2014). Compact Watershed and\n           Preemptive SLIC: On Improving Trade-offs of Superpixel Segmentation\n           Algorithms. ICPR 2014, pp 996-1001. DOI:10.1109/ICPR.2014.181\n           https://www.tu-chemnitz.de/etit/proaut/forschung/rsrc/cws_pSLIC_ICPR.pdf\n\n    Examples\n    --------\n    The watershed algorithm is useful to separate overlapping objects.\n\n    We first generate an initial image with two overlapping circles:\n\n    >>> x, y = np.indices((80, 80))\n    >>> x1, y1, x2, y2 = 28, 28, 44, 52\n    >>> r1, r2 = 16, 20\n    >>> mask_circle1 = (x - x1)**2 + (y - y1)**2 < r1**2\n    >>> mask_circle2 = (x - x2)**2 + (y - y2)**2 < r2**2\n    >>> image = np.logical_or(mask_circle1, mask_circle2)\n\n    Next, we want to separate the two circles. We generate markers at the\n    maxima of the distance to the background:\n\n    >>> from scipy import ndimage as ndi\n    >>> distance = ndi.distance_transform_edt(image)\n    >>> from skimage.feature import peak_local_max\n    >>> local_maxi = peak_local_max(distance, labels=image,\n    ...                             footprint=np.ones((3, 3)),\n    ...                             indices=False)\n    >>> markers = ndi.label(local_maxi)[0]\n\n    Finally, we run the watershed on the image and markers:\n\n    >>> labels = watershed(-distance, markers, mask=image)\n\n    The algorithm works also for 3-D images, and can be used for example to\n    separate overlapping spheres.\n    '
    (image, markers, mask) = _validate_inputs(image, markers, mask)
    (connectivity, offset) = _validate_connectivity(image.ndim, connectivity, offset)
    pad_width = [(p, p) for p in offset]
    image = np.pad(image, pad_width, mode='constant')
    mask = np.pad(mask, pad_width, mode='constant').ravel()
    output = np.pad(markers, pad_width, mode='constant')
    flat_neighborhood = _compute_neighbors(image, connectivity, offset)
    marker_locations = np.flatnonzero(output)
    image_strides = (np.array(image.strides, dtype=np.intp) // image.itemsize)
    _watershed.watershed_raveled(image.ravel(), marker_locations, flat_neighborhood, mask, image_strides, compactness, output.ravel(), watershed_line)
    output = crop(output, pad_width, copy=True)
    return output