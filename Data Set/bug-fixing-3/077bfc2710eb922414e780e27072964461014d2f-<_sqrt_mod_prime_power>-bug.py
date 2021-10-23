def _sqrt_mod_prime_power(a, p, k):
    '\n    find the solutions to ``x**2 = a mod p**k`` when ``a % p != 0``\n\n    Parameters\n    ==========\n\n    a : integer\n    p : prime number\n    k : positive integer\n\n    References\n    ==========\n\n    [1] P. Hackman "Elementary Number Theory" (2009),  page 160\n    [2] http://www.numbertheory.org/php/squareroot.html\n    [3] [Gathen99]_\n\n    Examples\n    ========\n\n    >>> from sympy.ntheory.residue_ntheory import _sqrt_mod_prime_power\n    >>> _sqrt_mod_prime_power(11, 43, 1)\n    [21, 22]\n    '
    from sympy.core.numbers import igcdex
    from sympy.polys.domains import ZZ
    pk = (p ** k)
    a = (a % pk)
    if (k == 1):
        if (p == 2):
            return [ZZ(a)]
        if (not is_quad_residue(a, p)):
            return None
        if ((p % 4) == 3):
            res = pow(a, ((p + 1) // 4), p)
        elif ((p % 8) == 5):
            sign = pow(a, ((p - 1) // 4), p)
            if (sign == 1):
                res = pow(a, ((p + 3) // 8), p)
            else:
                b = pow((4 * a), ((p - 5) // 8), p)
                x = (((2 * a) * b) % p)
                if (pow(x, 2, p) == a):
                    res = x
        else:
            res = _sqrt_mod_tonelli_shanks(a, p)
        return sorted([ZZ(res), ZZ((p - res))])
    if (k > 1):
        if (p == 2):
            if ((a % 8) != 1):
                return None
            if (k <= 3):
                s = set()
                for i in range(0, pk, 4):
                    s.add((1 + i))
                    s.add(((- 1) + i))
                return list(s)
            rv = [ZZ(1), ZZ(3), ZZ(5), ZZ(7)]
            n = 3
            res = []
            for r in rv:
                nx = n
                while (nx < k):
                    r1 = (((r ** 2) - a) >> nx)
                    if (r1 % 2):
                        r = (r + (1 << (nx - 1)))
                    nx += 1
                if (r not in res):
                    res.append(r)
                x = (r + (1 << (k - 1)))
                if ((x < (1 << nx)) and (x not in res)):
                    if ((((x ** 2) - a) % pk) == 0):
                        res.append(x)
            return res
        rv = _sqrt_mod_prime_power(a, p, 1)
        if (not rv):
            return None
        r = rv[0]
        fr = ((r ** 2) - a)
        n = 1
        px = p
        while 1:
            n1 = n
            n1 *= 2
            if (n1 > k):
                break
            n = n1
            px = (px ** 2)
            frinv = igcdex((2 * r), px)[0]
            r = ((r - (fr * frinv)) % px)
            fr = ((r ** 2) - a)
        if (n < k):
            px = (p ** k)
            frinv = igcdex((2 * r), px)[0]
            r = ((r - (fr * frinv)) % px)
        return [r, (px - r)]