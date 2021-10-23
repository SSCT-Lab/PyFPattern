def sqrt_mod_iter(a, p, domain=int):
    '\n    iterate over solutions to ``x**2 = a mod p``\n\n    Parameters\n    ==========\n\n    a : integer\n    p : positive integer\n    domain : integer domain, ``int``, ``ZZ`` or ``Integer``\n\n    Examples\n    ========\n\n    >>> from sympy.ntheory.residue_ntheory import sqrt_mod_iter\n    >>> list(sqrt_mod_iter(11, 43))\n    [21, 22]\n    '
    from sympy.polys.galoistools import gf_crt1, gf_crt2
    from sympy.polys.domains import ZZ
    (a, p) = (as_int(a), abs(as_int(p)))
    if isprime(p):
        a = (a % p)
        if (a == 0):
            res = _sqrt_mod1(a, p, 1)
        else:
            res = _sqrt_mod_prime_power(a, p, 1)
        if res:
            if (domain is ZZ):
                for x in res:
                    (yield x)
            else:
                for x in res:
                    (yield domain(x))
    else:
        f = factorint(p)
        v = []
        pv = []
        for (px, ex) in f.items():
            if ((a % px) == 0):
                rx = _sqrt_mod1(a, px, ex)
                if (not rx):
                    raise StopIteration
            else:
                rx = _sqrt_mod_prime_power(a, px, ex)
                if (not rx):
                    raise StopIteration
            v.append(rx)
            pv.append((px ** ex))
        (mm, e, s) = gf_crt1(pv, ZZ)
        if (domain is ZZ):
            for vx in _product(*v):
                r = gf_crt2(vx, pv, mm, e, s, ZZ)
                (yield r)
        else:
            for vx in _product(*v):
                r = gf_crt2(vx, pv, mm, e, s, ZZ)
                (yield domain(r))