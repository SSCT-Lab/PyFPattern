def invresz(r, p, k, tol=0.001, rtype='avg'):
    "\n    Compute b(z) and a(z) from partial fraction expansion.\n\n    If `M` is the degree of numerator `b` and `N` the degree of denominator\n    `a`::\n\n                b(z)     b[0] + b[1] z**(-1) + ... + b[M] z**(-M)\n        H(z) = ------ = ------------------------------------------\n                a(z)     a[0] + a[1] z**(-1) + ... + a[N] z**(-N)\n\n    then the partial-fraction expansion H(z) is defined as::\n\n                 r[0]                   r[-1]\n         = --------------- + ... + ---------------- + k[0] + k[1]z**(-1) ...\n           (1-p[0]z**(-1))         (1-p[-1]z**(-1))\n\n    If there are any repeated roots (closer than `tol`), then the partial\n    fraction expansion has terms like::\n\n             r[i]              r[i+1]                    r[i+n-1]\n        -------------- + ------------------ + ... + ------------------\n        (1-p[i]z**(-1))  (1-p[i]z**(-1))**2         (1-p[i]z**(-1))**n\n\n    This function is used for polynomials in negative powers of z,\n    such as digital filters in DSP.  For positive powers, use `invres`.\n\n    Parameters\n    ----------\n    r : array_like\n        Residues.\n    p : array_like\n        Poles.\n    k : array_like\n        Coefficients of the direct polynomial term.\n    tol : float, optional\n        The tolerance for two roots to be considered equal. Default is 1e-3.\n    rtype : {'max', 'min, 'avg'}, optional\n        How to determine the returned root if multiple roots are within\n        `tol` of each other.\n\n          - 'max': pick the maximum of those roots.\n          - 'min': pick the minimum of those roots.\n          - 'avg': take the average of those roots.\n\n    Returns\n    -------\n    b : ndarray\n        Numerator polynomial coefficients.\n    a : ndarray\n        Denominator polynomial coefficients.\n\n    See Also\n    --------\n    residuez, unique_roots, invres\n\n    "
    extra = np.asarray(k)
    (p, indx) = cmplx_sort(p)
    r = np.take(r, indx, 0)
    (pout, mult) = unique_roots(p, tol=tol, rtype=rtype)
    p = []
    for k in range(len(pout)):
        p.extend(([pout[k]] * mult[k]))
    a = np.atleast_1d(np.poly(p))
    if (len(extra) > 0):
        b = np.polymul(extra, a)
    else:
        b = [0]
    indx = 0
    brev = np.asarray(b)[::(- 1)]
    for k in range(len(pout)):
        temp = []
        for l in range(len(pout)):
            if (l != k):
                temp.extend(([pout[l]] * mult[l]))
        for m in range(mult[k]):
            t2 = temp[:]
            t2.extend(([pout[k]] * ((mult[k] - m) - 1)))
            brev = np.polyadd(brev, (r[indx] * np.atleast_1d(np.poly(t2)))[::(- 1)])
            indx += 1
    b = np.real_if_close(brev[::(- 1)])
    return (b, a)