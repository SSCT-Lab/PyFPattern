

def array_split(ary, indices_or_sections, axis=0):
    'Splits an array into multiple sub arrays along a given axis.\n\n    This function is almost equivalent to :func:`cupy.split`. The only\n    difference is that this function allows an integer sections that does not\n    evenly divide the axis.\n\n    .. seealso:: :func:`cupy.split` for more detail, :func:`numpy.array_split`\n\n    '
    if (ary.ndim <= axis):
        raise IndexError('Axis exceeds ndim')
    size = ary.shape[axis]
    if numpy.isscalar(indices_or_sections):
        each_size = (((size - 1) // indices_or_sections) + 1)
        indices = [(i * each_size) for i in six.moves.range(1, indices_or_sections)]
    else:
        indices = indices_or_sections
    if (len(indices) == 0):
        return [ary]
    skip = ((slice(None),) * axis)
    ret = []
    i = 0
    for index in indices:
        ret.append(ary[(skip + (slice(i, index),))])
        i = index
    ret.append(ary[(skip + (slice(i, size),))])
    return ret
