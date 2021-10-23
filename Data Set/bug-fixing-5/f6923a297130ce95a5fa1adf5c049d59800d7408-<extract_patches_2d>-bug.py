def extract_patches_2d(image, patch_size, max_patches=None, random_state=None):
    'Reshape a 2D image into a collection of patches\n\n    The resulting patches are allocated in a dedicated array.\n\n    Read more in the :ref:`User Guide <image_feature_extraction>`.\n\n    Parameters\n    ----------\n    image : array, shape = (image_height, image_width) or\n        (image_height, image_width, n_channels)\n        The original image data. For color images, the last dimension specifies\n        the channel: a RGB image would have `n_channels=3`.\n\n    patch_size : tuple of ints (patch_height, patch_width)\n        the dimensions of one patch\n\n    max_patches : integer or float, optional default is None\n        The maximum number of patches to extract. If max_patches is a float\n        between 0 and 1, it is taken to be a proportion of the total number\n        of patches.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        Pseudo number generator state used for random sampling to use if\n        `max_patches` is not None.  If int, random_state is the seed used by\n        the random number generator; If RandomState instance, random_state is\n        the random number generator; If None, the random number generator is\n        the RandomState instance used by `np.random`.\n\n    Returns\n    -------\n    patches : array, shape = (n_patches, patch_height, patch_width) or\n        (n_patches, patch_height, patch_width, n_channels)\n        The collection of patches extracted from the image, where `n_patches`\n        is either `max_patches` or the total number of patches that can be\n        extracted.\n\n    Examples\n    --------\n    >>> from sklearn.datasets import load_sample_image\n    >>> from sklearn.feature_extraction import image\n    >>> # Use the array data from the first image in this dataset:\n    >>> one_image = load_sample_image("china.jpg")\n    >>> print(\'Image shape: {}\'.format(one_image.shape))\n    Image shape: (427, 640, 3)\n    >>> patches = image.extract_patches_2d(one_image, (2, 2))\n    >>> print(\'Patches shape: {}\'.format(patches.shape))\n    Patches shape: (272214, 2, 2, 3)\n    >>> # Here are just two of these patches:\n    >>> print(patches[1])\n    [[[174 201 231]\n      [174 201 231]]\n     [[173 200 230]\n      [173 200 230]]]\n    >>> print(patches[800])\n    [[[187 214 243]\n      [188 215 244]]\n     [[187 214 243]\n      [188 215 244]]]\n    '
    (i_h, i_w) = image.shape[:2]
    (p_h, p_w) = patch_size
    if (p_h > i_h):
        raise ValueError('Height of the patch should be less than the height of the image.')
    if (p_w > i_w):
        raise ValueError('Width of the patch should be less than the width of the image.')
    image = check_array(image, allow_nd=True)
    image = image.reshape((i_h, i_w, (- 1)))
    n_colors = image.shape[(- 1)]
    extracted_patches = extract_patches(image, patch_shape=(p_h, p_w, n_colors), extraction_step=1)
    n_patches = _compute_n_patches(i_h, i_w, p_h, p_w, max_patches)
    if max_patches:
        rng = check_random_state(random_state)
        i_s = rng.randint(((i_h - p_h) + 1), size=n_patches)
        j_s = rng.randint(((i_w - p_w) + 1), size=n_patches)
        patches = extracted_patches[(i_s, j_s, 0)]
    else:
        patches = extracted_patches
    patches = patches.reshape((- 1), p_h, p_w, n_colors)
    if (patches.shape[(- 1)] == 1):
        return patches.reshape((n_patches, p_h, p_w))
    else:
        return patches