

def _obtain_input_shape(input_shape, default_size, min_size, data_format, include_top, weights='imagenet'):
    "Internal utility to compute/validate an ImageNet model's input shape.\n\n    # Arguments\n        input_shape: either None (will return the default network input shape),\n            or a user-provided shape to be validated.\n        default_size: default input width/height for the model.\n        min_size: minimum input width/height accepted by the model.\n        data_format: image data format to use.\n        include_top: whether the model is expected to\n            be linked to a classifier via a Flatten layer.\n        weights: one of `None` (random initialization)\n            or 'imagenet' (pre-training on ImageNet).\n            If weights='imagenet' input channels must be equal to 3.\n\n    # Returns\n        An integer shape tuple (may include None entries).\n\n    # Raises\n        ValueError: in case of invalid argument values.\n    "
    if ((weights != 'imagenet') and (input_shape is not None) and (len(input_shape) == 3)):
        if (data_format == 'channels_first'):
            if ((input_shape[0] != 3) or (input_shape[0] != 1)):
                warnings.warn((('This model usually expects 1 or 3 input channels. However, it was passed ' + str(input_shape[0])) + ' input channels.'))
            default_shape = (input_shape[0], default_size, default_size)
        else:
            if ((input_shape[(- 1)] != 3) or (input_shape[(- 1)] != 1)):
                warnings.warn((('This model usually expects 1 or 3 input channels. However, it was passed ' + str(input_shape[(- 1)])) + ' input channels.'))
            default_shape = (default_size, default_size, input_shape[(- 1)])
    elif (data_format == 'channels_first'):
        default_shape = (3, default_size, default_size)
    else:
        default_shape = (default_size, default_size, 3)
    if include_top:
        if (input_shape is not None):
            if (input_shape != default_shape):
                raise ValueError((('When setting`include_top=True`, `input_shape` should be ' + str(default_shape)) + '.'))
        input_shape = default_shape
    elif (data_format == 'channels_first'):
        if (input_shape is not None):
            if (len(input_shape) != 3):
                raise ValueError('`input_shape` must be a tuple of three integers.')
            if ((input_shape[0] != 3) and (weights == 'imagenet')):
                raise ValueError((('The input must have 3 channels; got `input_shape=' + str(input_shape)) + '`'))
            if (((input_shape[1] is not None) and (input_shape[1] < min_size)) or ((input_shape[2] is not None) and (input_shape[2] < min_size))):
                raise ValueError((((((('Input size must be at least ' + str(min_size)) + 'x') + str(min_size)) + ', got `input_shape=') + str(input_shape)) + '`'))
        else:
            input_shape = (3, None, None)
    elif (input_shape is not None):
        if (len(input_shape) != 3):
            raise ValueError('`input_shape` must be a tuple of three integers.')
        if ((input_shape[(- 1)] != 3) and (weights == 'imagenet')):
            raise ValueError((('The input must have 3 channels; got `input_shape=' + str(input_shape)) + '`'))
        if (((input_shape[0] is not None) and (input_shape[0] < min_size)) or ((input_shape[1] is not None) and (input_shape[1] < min_size))):
            raise ValueError((((((('Input size must be at least ' + str(min_size)) + 'x') + str(min_size)) + ', got `input_shape=') + str(input_shape)) + '`'))
    else:
        input_shape = (None, None, 3)
    return input_shape
