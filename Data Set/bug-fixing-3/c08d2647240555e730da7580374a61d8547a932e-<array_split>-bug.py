def array_split(ary, indices_or_sections, axis=0):
    '\n    Split an array into multiple sub-arrays.\n\n    Please refer to the ``split`` documentation.  The only difference\n    between these functions is that ``array_split`` allows\n    `indices_or_sections` to be an integer that does *not* equally\n    divide the axis. For an array of length l that should be split \n    into n sections, it returns l % n sub-arrays of size l//n + 1 \n    and the rest of size l//n.\n\n    See Also\n    --------\n    split : Split array into multiple sub-arrays of equal size.\n\n    Examples\n    --------\n    >>> x = np.arange(8.0)\n    >>> np.array_split(x, 3)\n        [array([ 0.,  1.,  2.]), array([ 3.,  4.,  5.]), array([ 6.,  7.])]\n\n    >>> x = np.arange(7.0)\n    >>> np.array_split(x, 3)\n        [array([ 0.,  1.,  2.]), array([ 3.,  4.]), array([ 5.,  6.])]\n\n    '
    try:
        Ntotal = ary.shape[axis]
    except AttributeError:
        Ntotal = len(ary)
    try:
        Nsections = (len(indices_or_sections) + 1)
        div_points = (([0] + list(indices_or_sections)) + [Ntotal])
    except TypeError:
        Nsections = int(indices_or_sections)
        if (Nsections <= 0):
            raise ValueError('number sections must be larger than 0.')
        (Neach_section, extras) = divmod(Ntotal, Nsections)
        section_sizes = (([0] + (extras * [(Neach_section + 1)])) + ((Nsections - extras) * [Neach_section]))
        div_points = _nx.array(section_sizes).cumsum()
    sub_arys = []
    sary = _nx.swapaxes(ary, axis, 0)
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[(i + 1)]
        sub_arys.append(_nx.swapaxes(sary[st:end], axis, 0))
    return sub_arys