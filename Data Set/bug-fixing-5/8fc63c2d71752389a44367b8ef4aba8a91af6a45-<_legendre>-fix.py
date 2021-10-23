def _legendre(a, p):
    '\n    Returns the legendre symbol of a and p\n    assuming that p is a prime\n\n    i.e. 1 if a is a quadratic residue mod p\n        -1 if a is not a quadratic residue mod p\n         0 if a is divisible by p\n\n    Parameters\n    ==========\n\n    a : int the number to test\n    p : the prime to test a against\n\n    Returns\n    =======\n\n    legendre symbol (a / p) (int)\n\n    '
    sig = pow(a, ((p - 1) // 2), p)
    if (sig == 1):
        return 1
    elif (sig == 0):
        return 0
    else:
        return (- 1)