def get_fans(shape):
    if (not isinstance(shape, tuple)):
        raise ValueError('shape must be tuple')
    if (len(shape) < 2):
        raise ValueError('shape must be of length >= 2: shape={}', shape)
    receptive_field_size = utils.size_of_shape(shape[2:])
    fan_in = (shape[1] * receptive_field_size)
    fan_out = (shape[0] * receptive_field_size)
    return (fan_in, fan_out)