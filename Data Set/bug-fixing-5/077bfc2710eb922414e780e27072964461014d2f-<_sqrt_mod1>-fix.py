def _sqrt_mod1(a, p, n):
    '\n    Find solution to ``x**2 == a mod p**n`` when ``a % p == 0``\n\n    see http://www.numbertheory.org/php/squareroot.html\n    '
    pn = (p ** n)
    a = (a % pn)
    if (a == 0):
        m = (n // 2)
        if ((n % 2) == 1):
            pm1 = (p ** (m + 1))

            def _iter0a():
                i = 0
                while (i < pn):
                    (yield i)
                    i += pm1
            return _iter0a()
        else:
            pm = (p ** m)

            def _iter0b():
                i = 0
                while (i < pn):
                    (yield i)
                    i += pm
            return _iter0b()
    f = factorint(a)
    r = f[p]
    if ((r % 2) == 1):
        return None
    m = (r // 2)
    a1 = (a >> r)
    if (p == 2):
        if ((n - r) == 1):
            pnm1 = (1 << ((n - m) + 1))
            pm1 = (1 << (m + 1))

            def _iter1():
                k = (1 << (m + 2))
                i = (1 << m)
                while (i < pnm1):
                    j = i
                    while (j < pn):
                        (yield j)
                        j += k
                    i += pm1
            return _iter1()
        if ((n - r) == 2):
            res = _sqrt_mod_prime_power(a1, p, (n - r))
            if (res is None):
                return None
            pnm = (1 << (n - m))

            def _iter2():
                s = set()
                for r in res:
                    i = 0
                    while (i < pn):
                        x = ((r << m) + i)
                        if (x not in s):
                            s.add(x)
                            (yield x)
                        i += pnm
            return _iter2()
        if ((n - r) > 2):
            res = _sqrt_mod_prime_power(a1, p, (n - r))
            if (res is None):
                return None
            pnm1 = (1 << ((n - m) - 1))

            def _iter3():
                s = set()
                for r in res:
                    i = 0
                    while (i < pn):
                        x = (((r << m) + i) % pn)
                        if (x not in s):
                            s.add(x)
                            (yield x)
                        i += pnm1
            return _iter3()
    else:
        m = (r // 2)
        a1 = (a // (p ** r))
        res1 = _sqrt_mod_prime_power(a1, p, (n - r))
        if (res1 is None):
            return None
        pm = (p ** m)
        pnr = (p ** (n - r))
        pnm = (p ** (n - m))

        def _iter4():
            s = set()
            pm = (p ** m)
            for rx in res1:
                i = 0
                while (i < pnm):
                    x = ((rx + i) % pn)
                    if (x not in s):
                        s.add(x)
                        (yield (x * pm))
                    i += pnr
        return _iter4()