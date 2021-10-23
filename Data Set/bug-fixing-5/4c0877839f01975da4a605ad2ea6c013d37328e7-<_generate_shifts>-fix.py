def _generate_shifts(ndim, multichannel, max_shifts, shift_steps=1):
    'Returns all combinations of shifts in n dimensions over the specified\n    max_shifts and step sizes.\n\n    Examples\n    --------\n    >>> s = list(_generate_shifts(2, False, max_shifts=(1, 2), shift_steps=1))\n    >>> print(s)\n    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]\n    '
    mc = int(multichannel)
    if np.isscalar(max_shifts):
        max_shifts = (((max_shifts,) * (ndim - mc)) + ((0,) * mc))
    elif (multichannel and (len(max_shifts) == (ndim - 1))):
        max_shifts = (tuple(max_shifts) + (0,))
    elif (len(max_shifts) != ndim):
        raise ValueError('max_shifts should have length ndim')
    if np.isscalar(shift_steps):
        shift_steps = (((shift_steps,) * (ndim - mc)) + ((1,) * mc))
    elif (multichannel and (len(shift_steps) == (ndim - 1))):
        shift_steps = (tuple(shift_steps) + (1,))
    elif (len(shift_steps) != ndim):
        raise ValueError('max_shifts should have length ndim')
    if any(((s < 1) for s in shift_steps)):
        raise ValueError('shift_steps must all be >= 1')
    if (multichannel and (max_shifts[(- 1)] != 0)):
        raise ValueError('Multichannel cycle spinning should not have shifts along the last axis.')
    return product(*[range(0, (s + 1), t) for (s, t) in zip(max_shifts, shift_steps)])