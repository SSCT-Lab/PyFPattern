

def inpaint_biharmonic(image, mask, multichannel=False):
    'Inpaint masked points in image with biharmonic equations.\n\n    Parameters\n    ----------\n    image : (M[, N[, ..., P]][, C]) ndarray\n        Input image.\n    mask : (M[, N[, ..., P]]) ndarray\n        Array of pixels to be inpainted. Have to be the same shape as one\n        of the \'image\' channels. Unknown pixels have to be represented with 1,\n        known pixels - with 0.\n    multichannel : boolean, optional\n        If True, the last `image` dimension is considered as a color channel,\n        otherwise as spatial.\n\n    Returns\n    -------\n    out : (M[, N[, ..., P]][, C]) ndarray\n        Input image with masked pixels inpainted.\n\n    References\n    ----------\n    .. [1]  N.S.Hoang, S.B.Damelin, "On surface completion and image inpainting\n            by biharmonic functions: numerical aspects",\n            http://www.ima.umn.edu/~damelin/biharmonic\n\n    Examples\n    --------\n    >>> img = np.tile(np.square(np.linspace(0, 1, 5)), (5, 1))\n    >>> mask = np.zeros_like(img)\n    >>> mask[2, 2:] = 1\n    >>> mask[1, 3:] = 1\n    >>> mask[0, 4:] = 1\n    >>> out = inpaint_biharmonic(img, mask)\n    '
    if (image.ndim < 1):
        raise ValueError('Input array has to be at least 1D')
    img_baseshape = (image.shape[:(- 1)] if multichannel else image.shape)
    if (img_baseshape != mask.shape):
        raise ValueError('Input arrays have to be the same shape')
    if np.ma.isMaskedArray(image):
        raise TypeError('Masked arrays are not supported')
    image = skimage.img_as_float(image)
    mask = mask.astype(np.bool)
    kernel = ndi.morphology.generate_binary_structure(mask.ndim, 1)
    mask_dilated = ndi.morphology.binary_dilation(mask, structure=kernel)
    (mask_labeled, num_labels) = label(mask_dilated, return_num=True)
    mask_labeled *= mask
    if (not multichannel):
        image = image[(..., np.newaxis)]
    out = np.copy(image)
    for idx_channel in range(image.shape[(- 1)]):
        known_points = image[(..., idx_channel)][(~ mask)]
        limits = (np.min(known_points), np.max(known_points))
        for idx_region in range(1, (num_labels + 1)):
            mask_region = (mask_labeled == idx_region)
            _inpaint_biharmonic_single_channel(mask_region, out[(..., idx_channel)], limits)
    if (not multichannel):
        out = out[(..., 0)]
    return out
