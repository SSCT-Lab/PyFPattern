def slic(image, n_segments=100, compactness=10.0, max_iter=10, sigma=0, spacing=None, multichannel=True, convert2lab=None, enforce_connectivity=True, min_size_factor=0.5, max_size_factor=3, slic_zero=False):
    'Segments image using k-means clustering in Color-(x,y,z) space.\n\n    Parameters\n    ----------\n    image : 2D, 3D or 4D ndarray\n        Input image, which can be 2D or 3D, and grayscale or multichannel\n        (see `multichannel` parameter).\n    n_segments : int, optional\n        The (approximate) number of labels in the segmented output image.\n    compactness : float, optional\n        Balances color proximity and space proximity. Higher values give\n        more weight to space proximity, making superpixel shapes more\n        square/cubic. In SLICO mode, this is the initial compactness.\n        This parameter depends strongly on image contrast and on the\n        shapes of objects in the image. We recommend exploring possible\n        values on a log scale, e.g., 0.01, 0.1, 1, 10, 100, before\n        refining around a chosen value.\n    max_iter : int, optional\n        Maximum number of iterations of k-means.\n    sigma : float or (3,) array-like of floats, optional\n        Width of Gaussian smoothing kernel for pre-processing for each\n        dimension of the image. The same sigma is applied to each dimension in\n        case of a scalar value. Zero means no smoothing.\n        Note, that `sigma` is automatically scaled if it is scalar and a\n        manual voxel spacing is provided (see Notes section).\n    spacing : (3,) array-like of floats, optional\n        The voxel spacing along each image dimension. By default, `slic`\n        assumes uniform spacing (same voxel resolution along z, y and x).\n        This parameter controls the weights of the distances along z, y,\n        and x during k-means clustering.\n    multichannel : bool, optional\n        Whether the last axis of the image is to be interpreted as multiple\n        channels or another spatial dimension.\n    convert2lab : bool, optional\n        Whether the input should be converted to Lab colorspace prior to\n        segmentation. The input image *must* be RGB. Highly recommended.\n        This option defaults to ``True`` when ``multichannel=True`` *and*\n        ``image.shape[-1] == 3``.\n    enforce_connectivity: bool, optional\n        Whether the generated segments are connected or not\n    min_size_factor: float, optional\n        Proportion of the minimum segment size to be removed with respect\n        to the supposed segment size ```depth*width*height/n_segments```\n    max_size_factor: float, optional\n        Proportion of the maximum connected segment size. A value of 3 works\n        in most of the cases.\n    slic_zero: bool, optional\n        Run SLIC-zero, the zero-parameter mode of SLIC. [2]_\n\n    Returns\n    -------\n    labels : 2D or 3D array\n        Integer mask indicating segment labels.\n\n    Raises\n    ------\n    ValueError\n        If ``convert2lab`` is set to ``True`` but the last array\n        dimension is not of length 3.\n\n    Notes\n    -----\n    * If `sigma > 0`, the image is smoothed using a Gaussian kernel prior to\n      segmentation.\n\n    * If `sigma` is scalar and `spacing` is provided, the kernel width is\n      divided along each dimension by the spacing. For example, if ``sigma=1``\n      and ``spacing=[5, 1, 1]``, the effective `sigma` is ``[0.2, 1, 1]``. This\n      ensures sensible smoothing for anisotropic images.\n\n    * The image is rescaled to be in [0, 1] prior to processing.\n\n    * Images of shape (M, N, 3) are interpreted as 2D RGB images by default. To\n      interpret them as 3D with the last dimension having length 3, use\n      `multichannel=False`.\n\n    References\n    ----------\n    .. [1] Radhakrishna Achanta, Appu Shaji, Kevin Smith, Aurelien Lucchi,\n        Pascal Fua, and Sabine Süsstrunk, SLIC Superpixels Compared to\n        State-of-the-art Superpixel Methods, TPAMI, May 2012.\n    .. [2] http://ivrg.epfl.ch/research/superpixels#SLICO\n\n    Examples\n    --------\n    >>> from skimage.segmentation import slic\n    >>> from skimage.data import astronaut\n    >>> img = astronaut()\n    >>> segments = slic(img, n_segments=100, compactness=10)\n\n    Increasing the compactness parameter yields more square regions:\n\n    >>> segments = slic(img, n_segments=100, compactness=20)\n\n    '
    image = img_as_float(image)
    is_2d = False
    if (image.ndim == 2):
        image = image[(np.newaxis, ..., np.newaxis)]
        is_2d = True
    elif ((image.ndim == 3) and multichannel):
        image = image[(np.newaxis, ...)]
        is_2d = True
    elif ((image.ndim == 3) and (not multichannel)):
        image = image[(..., np.newaxis)]
    if (spacing is None):
        spacing = np.ones(3)
    elif isinstance(spacing, (list, tuple)):
        spacing = np.array(spacing, dtype=np.double)
    if (not isinstance(sigma, Iterable)):
        sigma = np.array([sigma, sigma, sigma], dtype=np.double)
        sigma /= spacing.astype(np.double)
    elif isinstance(sigma, (list, tuple)):
        sigma = np.array(sigma, dtype=np.double)
    if (sigma > 0).any():
        sigma = (list(sigma) + [0])
        image = ndi.gaussian_filter(image, sigma)
    if (multichannel and (convert2lab or (convert2lab is None))):
        if ((image.shape[(- 1)] != 3) and convert2lab):
            raise ValueError('Lab colorspace conversion requires a RGB image.')
        elif (image.shape[(- 1)] == 3):
            image = rgb2lab(image)
    (depth, height, width) = image.shape[:3]
    (grid_z, grid_y, grid_x) = np.mgrid[:depth, :height, :width]
    slices = regular_grid(image.shape[:3], n_segments)
    (step_z, step_y, step_x) = [int((s.step if (s.step is not None) else 1)) for s in slices]
    segments_z = grid_z[slices]
    segments_y = grid_y[slices]
    segments_x = grid_x[slices]
    segments_color = np.zeros((segments_z.shape + (image.shape[3],)))
    segments = np.concatenate([segments_z[(..., np.newaxis)], segments_y[(..., np.newaxis)], segments_x[(..., np.newaxis)], segments_color], axis=(- 1)).reshape((- 1), (3 + image.shape[3]))
    segments = np.ascontiguousarray(segments)
    step = float(max((step_z, step_y, step_x)))
    ratio = (1.0 / compactness)
    image = np.ascontiguousarray((image * ratio))
    labels = _slic_cython(image, segments, step, max_iter, spacing, slic_zero)
    if enforce_connectivity:
        segment_size = (((depth * height) * width) / n_segments)
        min_size = int((min_size_factor * segment_size))
        max_size = int((max_size_factor * segment_size))
        labels = _enforce_label_connectivity_cython(labels, min_size, max_size)
    if is_2d:
        labels = labels[0]
    return labels