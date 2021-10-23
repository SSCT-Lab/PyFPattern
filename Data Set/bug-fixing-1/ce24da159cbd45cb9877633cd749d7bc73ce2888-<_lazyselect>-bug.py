

def _lazyselect(condlist, choicelist, arrays, default=0):
    '\n    Mimic `np.select(condlist, choicelist)`.\n\n    Notice it assumes that all `arrays` are of the same shape, or can be\n    broadcasted together.\n\n    All functions in `choicelist` must accept array arguments in the order\n    given in `arrays` and must return an array of the same shape as broadcasted\n    `arrays`.\n\n    Examples\n    --------\n    >>> x = np.arange(6)\n    >>> np.select([x <3, x > 3], [x**2, x**3], default=0)\n    array([  0,   1,   4,   0,  64, 125])\n\n    >>> _lazyselect([x < 3, x > 3], [lambda x: x**2, lambda x: x**3], (x,))\n    array([   0.,    1.,    4.,   nan,   64.,  125.])\n\n    >>> a = -np.ones_like(x)\n    >>> _lazyselect([x < 3, x > 3],\n    ...             [lambda x, a: x**2, lambda x, a: a * x**3],\n    ...             (x, a))\n    array([   0.,    1.,    4.,   nan,  -64., -125.])\n\n    '
    arrays = np.broadcast_arrays(*arrays)
    tcode = np.mintypecode([a.dtype.char for a in arrays])
    out = _valarray(np.shape(arrays[0]), value=default, typecode=tcode)
    for index in range(len(condlist)):
        (func, cond) = (choicelist[index], condlist[index])
        if np.all((cond is False)):
            continue
        (cond, _) = np.broadcast_arrays(cond, arrays[0])
        temp = tuple((np.extract(cond, arr) for arr in arrays))
        np.place(out, cond, func(*temp))
    return out
