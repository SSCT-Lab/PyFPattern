def nthroot_mod(a, n, p, all_roots=False):
    '\n    Find the solutions to ``x**n = a mod p``\n\n    Parameters\n    ==========\n\n    a : integer\n    n : positive integer\n    p : positive integer\n    all_roots : if False returns the smallest root, else the list of roots\n\n    Examples\n    ========\n\n    >>> from sympy.ntheory.residue_ntheory import nthroot_mod\n    >>> nthroot_mod(11, 4, 19)\n    8\n    >>> nthroot_mod(11, 4, 19, True)\n    [8, 11]\n    >>> nthroot_mod(68, 3, 109)\n    23\n    '
    from sympy.core.numbers import igcdex
    if (n == 2):
        return sqrt_mod(a, p, all_roots)
    f = totient(p)
    if (not is_nthpow_residue(a, n, p)):
        return None
    if (primitive_root(p) == None):
        raise NotImplementedError('Not Implemented for m without primitive root')
    if (((p - 1) % n) == 0):
        return _nthroot_mod1(a, n, p, all_roots)
    pa = n
    pb = (p - 1)
    b = 1
    if (pa < pb):
        (a, pa, b, pb) = (b, pb, a, pa)
    while pb:
        (q, r) = divmod(pa, pb)
        c = pow(b, q, p)
        c = igcdex(c, p)[0]
        c = ((c * a) % p)
        (pa, pb) = (pb, r)
        (a, b) = (b, c)
    if (pa == 1):
        if all_roots:
            res = [a]
        else:
            res = a
    elif (pa == 2):
        return sqrt_mod(a, p, all_roots)
    else:
        res = _nthroot_mod1(a, pa, p, all_roots)
    return res