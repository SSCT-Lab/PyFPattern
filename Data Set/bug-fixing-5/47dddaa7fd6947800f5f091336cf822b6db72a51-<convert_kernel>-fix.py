def convert_kernel(kernel):
    'Converts a Numpy kernel matrix from Theano format to TensorFlow format.\n\n    Also works reciprocally, since the transformation is its own inverse.\n\n    # Arguments\n        kernel: Numpy array (3D, 4D or 5D).\n\n    # Returns\n        The converted kernel.\n\n    # Raises\n        ValueError: in case of invalid kernel shape or invalid data_format.\n    '
    kernel = np.asarray(kernel)
    if (not (3 <= kernel.ndim <= 5)):
        raise ValueError('Invalid kernel shape:', kernel.shape)
    slices = [slice(None, None, (- 1)) for _ in range(kernel.ndim)]
    no_flip = (slice(None, None), slice(None, None))
    slices[(- 2):] = no_flip
    return np.copy(kernel[slices])