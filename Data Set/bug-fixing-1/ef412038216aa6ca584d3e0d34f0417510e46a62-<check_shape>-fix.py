

def check_shape(args, current_shape=None):
    'Imitate numpy.matrix handling of shape arguments'
    if (len(args) == 0):
        raise TypeError("function missing 1 required positional argument: 'shape'")
    elif (len(args) == 1):
        try:
            shape_iter = iter(args[0])
        except TypeError:
            new_shape = (operator.index(args[0]),)
        else:
            new_shape = tuple((operator.index(arg) for arg in shape_iter))
    else:
        new_shape = tuple((operator.index(arg) for arg in args))
    if (current_shape is None):
        if (len(new_shape) != 2):
            raise ValueError('shape must be a 2-tuple of positive integers')
        elif ((new_shape[0] < 0) or (new_shape[1] < 0)):
            raise ValueError("'shape' elements cannot be negative")
    else:
        current_size = np.prod(current_shape, dtype=int)
        negative_indexes = [i for (i, x) in enumerate(new_shape) if (x < 0)]
        if (len(negative_indexes) == 0):
            new_size = np.prod(new_shape, dtype=int)
            if (new_size != current_size):
                raise ValueError('cannot reshape array of size {} into shape {}'.format(current_size, new_shape))
        elif (len(negative_indexes) == 1):
            skip = negative_indexes[0]
            specified = np.prod((new_shape[0:skip] + new_shape[(skip + 1):]))
            (unspecified, remainder) = divmod(current_size, specified)
            if (remainder != 0):
                err_shape = tuple((('newshape' if (x < 0) else x) for x in new_shape))
                raise ValueError('cannot reshape array of size {} into shape {}'.format(current_size, err_shape))
            new_shape = ((new_shape[0:skip] + (unspecified,)) + new_shape[(skip + 1):])
        else:
            raise ValueError('can only specify one unknown dimension')
        if (len(new_shape) != 2):
            new_shape = tuple((arg for arg in new_shape if (arg != 1)))
            if (len(new_shape) == 0):
                new_shape = (1, 1)
            elif (len(new_shape) == 1):
                new_shape = (1, new_shape[0])
    if (len(new_shape) > 2):
        raise ValueError('shape too large to be a matrix')
    return new_shape
