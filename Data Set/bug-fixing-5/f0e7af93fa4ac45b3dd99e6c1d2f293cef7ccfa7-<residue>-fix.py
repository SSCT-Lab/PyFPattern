def residue(b, a, tol=0.001, rtype='avg'):
    '\n    Compute partial-fraction expansion of b(s) / a(s).\n\n    If `M` is the degree of numerator `b` and `N` the degree of denominator\n    `a`::\n\n              b(s)     b[0] s**(M) + b[1] s**(M-1) + ... + b[M]\n      H(s) = ------ = ------------------------------------------\n              a(s)     a[0] s**(N) + a[1] s**(N-1) + ... + a[N]\n\n    then the partial-fraction expansion H(s) is defined as::\n\n               r[0]       r[1]             r[-1]\n           = -------- + -------- + ... + --------- + k(s)\n             (s-p[0])   (s-p[1])         (s-p[-1])\n\n    If there are any repeated roots (closer together than `tol`), then H(s)\n    has terms like::\n\n          r[i]      r[i+1]              r[i+n-1]\n        -------- + ----------- + ... + -----------\n        (s-p[i])  (s-p[i])**2          (s-p[i])**n\n\n    This function is used for polynomials in positive powers of s or z,\n    such as analog filters or digital filters in controls engineering.  For\n    negative powers of z (typical for digital filters in DSP), use `residuez`.\n\n    Parameters\n    ----------\n    b : array_like\n        Numerator polynomial coefficients.\n    a : array_like\n        Denominator polynomial coefficients.\n\n    Returns\n    -------\n    r : ndarray\n        Residues.\n    p : ndarray\n        Poles order by magnitude in ascending order.\n    k : ndarray\n        Coefficients of the direct polynomial term.\n\n    See Also\n    --------\n    invres, residuez, numpy.poly, unique_roots\n\n    '
    b = np.trim_zeros(np.atleast_1d(b), 'f')
    a = np.trim_zeros(np.atleast_1d(a), 'f')
    if (a.size == 0):
        raise ValueError('Denominator `a` is zero.')
    p = np.roots(a)
    if (b.size == 0):
        return (np.zeros(p.shape), p, np.array([]))
    rscale = a[0]
    (k, b) = np.polydiv(b, a)
    r = (p * 0.0)
    (pout, mult) = unique_roots(p, tol=tol, rtype=rtype)
    (pout, order) = cmplx_sort(pout)
    mult = mult[order]
    p = []
    for n in range(len(pout)):
        p.extend(([pout[n]] * mult[n]))
    p = np.asarray(p)
    indx = 0
    for n in range(len(pout)):
        bn = b.copy()
        pn = []
        for l in range(len(pout)):
            if (l != n):
                pn.extend(([pout[l]] * mult[l]))
        an = np.atleast_1d(np.poly(pn))
        sig = mult[n]
        for m in range(sig, 0, (- 1)):
            if (sig > m):
                term1 = np.polymul(np.polyder(bn, 1), an)
                term2 = np.polymul(bn, np.polyder(an, 1))
                bn = np.polysub(term1, term2)
                an = np.polymul(an, an)
            r[((indx + m) - 1)] = ((np.polyval(bn, pout[n]) / np.polyval(an, pout[n])) / factorial((sig - m)))
        indx += sig
    return ((r / rscale), p, np.trim_zeros(k, 'f'))