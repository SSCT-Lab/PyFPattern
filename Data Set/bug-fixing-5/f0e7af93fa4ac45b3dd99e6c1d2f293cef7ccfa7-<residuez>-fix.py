def residuez(b, a, tol=0.001, rtype='avg'):
    '\n    Compute partial-fraction expansion of b(z) / a(z).\n\n    If `M` is the degree of numerator `b` and `N` the degree of denominator\n    `a`::\n\n                b(z)     b[0] + b[1] z**(-1) + ... + b[M] z**(-M)\n        H(z) = ------ = ------------------------------------------\n                a(z)     a[0] + a[1] z**(-1) + ... + a[N] z**(-N)\n\n    then the partial-fraction expansion H(z) is defined as::\n\n                 r[0]                   r[-1]\n         = --------------- + ... + ---------------- + k[0] + k[1]z**(-1) ...\n           (1-p[0]z**(-1))         (1-p[-1]z**(-1))\n\n    If there are any repeated roots (closer than `tol`), then the partial\n    fraction expansion has terms like::\n\n             r[i]              r[i+1]                    r[i+n-1]\n        -------------- + ------------------ + ... + ------------------\n        (1-p[i]z**(-1))  (1-p[i]z**(-1))**2         (1-p[i]z**(-1))**n\n\n    This function is used for polynomials in negative powers of z,\n    such as digital filters in DSP.  For positive powers, use `residue`.\n\n    Parameters\n    ----------\n    b : array_like\n        Numerator polynomial coefficients.\n    a : array_like\n        Denominator polynomial coefficients.\n\n    Returns\n    -------\n    r : ndarray\n        Residues.\n    p : ndarray\n        Poles.\n    k : ndarray\n        Coefficients of the direct polynomial term.\n\n    See Also\n    --------\n    invresz, residue, unique_roots\n\n    '
    (b, a) = map(np.asarray, (b, a))
    gain = a[0]
    (brev, arev) = (b[::(- 1)], a[::(- 1)])
    (krev, brev) = np.polydiv(brev, arev)
    if (krev == []):
        k = []
    else:
        k = krev[::(- 1)]
    b = brev[::(- 1)]
    p = np.roots(a)
    r = (p * 0.0)
    (pout, mult) = unique_roots(p, tol=tol, rtype=rtype)
    p = []
    for n in range(len(pout)):
        p.extend(([pout[n]] * mult[n]))
    p = np.asarray(p)
    indx = 0
    for n in range(len(pout)):
        bn = brev.copy()
        pn = []
        for l in range(len(pout)):
            if (l != n):
                pn.extend(([pout[l]] * mult[l]))
        an = np.atleast_1d(np.poly(pn))[::(- 1)]
        sig = mult[n]
        for m in range(sig, 0, (- 1)):
            if (sig > m):
                term1 = np.polymul(np.polyder(bn, 1), an)
                term2 = np.polymul(bn, np.polyder(an, 1))
                bn = np.polysub(term1, term2)
                an = np.polymul(an, an)
            r[((indx + m) - 1)] = (((np.polyval(bn, (1.0 / pout[n])) / np.polyval(an, (1.0 / pout[n]))) / factorial((sig - m))) / ((- pout[n]) ** (sig - m)))
        indx += sig
    return ((r / gain), p, k)