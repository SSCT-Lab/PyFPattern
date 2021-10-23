def sqrt_mod(a, p, all_roots=False):
    '\n    find a root of ``x**2 = a mod p``\n\n    Parameters\n    ==========\n\n    a : integer\n    p : positive integer\n    all_roots : if True the list of roots is returned or None\n\n    Notes\n    =====\n\n    If there is no root it is returned None; else the returned root\n    is less or equal to ``p // 2``; in general is not the smallest one.\n    It is returned ``p // 2`` only if it is the only root.\n\n    Use ``all_roots`` only when it is expected that all the roots fit\n    in memory; otherwise use ``sqrt_mod_iter``.\n\n    Examples\n    ========\n\n    >>> from sympy.ntheory import sqrt_mod\n    >>> sqrt_mod(11, 43)\n    21\n    >>> sqrt_mod(17, 32, True)\n    [7, 9, 23, 25]\n    '
    if all_roots:
        return sorted(list(sqrt_mod_iter(a, p)))
    try:
        p = abs(as_int(p))
        it = sqrt_mod_iter(a, p)
        r = next(it)
        if (r > (p // 2)):
            return (p - r)
        elif (r < (p // 2)):
            return r
        else:
            try:
                r = next(it)
                if (r > (p // 2)):
                    return (p - r)
            except StopIteration:
                pass
            return r
    except StopIteration:
        return None