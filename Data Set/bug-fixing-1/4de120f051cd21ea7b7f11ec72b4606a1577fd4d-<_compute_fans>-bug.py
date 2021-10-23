

def _compute_fans(shape, data_format='channels_last'):
    'Computes the number of input and output units for a weight shape.\n\n    # Arguments\n        shape: Integer shape tuple.\n        data_format: Image data format to use for convolution kernels.\n            Note that all kernels in Keras are standardized on the\n            `channels_last` ordering (even when inputs are set\n            to `channels_first`).\n\n    # Returns\n        A tuple of scalars, `(fan_in, fan_out)`.\n\n    # Raises\n        ValueError: in case of invalid `data_format` argument.\n    '
    if (len(shape) == 2):
        fan_in = shape[0]
        fan_out = shape[1]
    elif (len(shape) in {3, 4, 5}):
        if (data_format == 'channels_first'):
            receptive_field_size = np.prod(shape[2:])
            fan_in = (shape[1] * receptive_field_size)
            fan_out = (shape[0] * receptive_field_size)
        elif (data_format == 'channels_last'):
            receptive_field_size = np.prod(shape[:2])
            fan_in = (shape[(- 2)] * receptive_field_size)
            fan_out = (shape[(- 1)] * receptive_field_size)
        else:
            raise ValueError(('Invalid data_format: ' + data_format))
    else:
        fan_in = np.sqrt(np.prod(shape))
        fan_out = np.sqrt(np.prod(shape))
    return (fan_in, fan_out)
