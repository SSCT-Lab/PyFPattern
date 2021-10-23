@tf_export('image.random_jpeg_quality')
def random_jpeg_quality(image, min_jpeg_quality, max_jpeg_quality, seed=None):
    'Randomly changes jpeg encoding quality for inducing jpeg noise.\n\n  `min_jpeg_quality` must be in the interval `[0, 100]` and less than\n  `max_jpeg_quality`.\n  `max_jpeg_quality` must be in the interval `[0, 100]`.\n\n  Args:\n    image: 3D image. Size of the last dimension must be 1 or 3.\n    min_jpeg_quality: Minimum jpeg encoding quality to use.\n    max_jpeg_quality: Maximum jpeg encoding quality to use.\n    seed: An operation-specific seed. It will be used in conjunction with the\n      graph-level seed to determine the real seeds that will be used in this\n      operation. Please see the documentation of set_random_seed for its\n      interaction with the graph-level random seed.\n\n  Returns:\n    Adjusted image(s), same shape and DType as `image`.\n\n  Raises:\n    ValueError: if `min_jpeg_quality` or `max_jpeg_quality` is invalid.\n  '
    if ((min_jpeg_quality < 0) or (max_jpeg_quality < 0) or (min_jpeg_quality > 100) or (max_jpeg_quality > 100)):
        raise ValueError('jpeg encoding range must be between 0 and 100.')
    if (min_jpeg_quality >= max_jpeg_quality):
        raise ValueError('`min_jpeg_quality` must be less than `max_jpeg_quality`.')
    if compat.forward_compatible(2019, 4, 4):
        jpeg_quality = random_ops.random_uniform([], min_jpeg_quality, max_jpeg_quality, seed=seed, dtype=dtypes.int32)
    else:
        np.random.seed(seed)
        jpeg_quality = np.random.randint(min_jpeg_quality, max_jpeg_quality)
    return adjust_jpeg_quality(image, jpeg_quality)