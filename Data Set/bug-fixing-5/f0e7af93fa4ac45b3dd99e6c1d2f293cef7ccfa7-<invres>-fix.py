def invres(r, p, k, tol=0.001, rtype='avg'):
    "\n    Compute b(s) and a(s) from partial fraction expansion.\n\n    If `M` is the degree of numerator `b` and `N` the degree of denominator\n    `a`::\n\n              b(s)     b[0] s**(M) + b[1] s**(M-1) + ... + b[M]\n      H(s) = ------ = ------------------------------------------\n              a(s)     a[0] s**(N) + a[1] s**(N-1) + ... + a[N]\n\n    then the partial-fraction expansion H(s) is defined as::\n\n               r[0]       r[1]             r[-1]\n           = -------- + -------- + ... + --------- + k(s)\n             (s-p[0])   (s-p[1])         (s-p[-1])\n\n    If there are any repeated roots (closer together than `tol`), then H(s)\n    has terms like::\n\n          r[i]      r[i+1]              r[i+n-1]\n        -------- + ----------- + ... + -----------\n        (s-p[i])  (s-p[i])**2          (s-p[i])**n\n\n    This function is used for polynomials in positive powers of s or z,\n    such as analog filters or digital filters in controls engineering.  For\n    negative powers of z (typical for digital filters in DSP), use `invresz`.\n\n    Parameters\n    ----------\n    r : array_like\n        Residues.\n    p : array_like\n        Poles.\n    k : array_like\n        Coefficients of the direct polynomial term.\n    tol : float, optional\n        The tolerance for two roots to be considered equal. Default is 1e-3.\n    rtype : {'max', 'min, 'avg'}, optional\n        How to determine the returned root if multiple roots are within\n        `tol` of each other.\n\n          - 'max': pick the maximum of those roots.\n          - 'min': pick the minimum of those roots.\n          - 'avg': take the average of those roots.\n\n    Returns\n    -------\n    b : ndarray\n        Numerator polynomial coefficients.\n    a : ndarray\n        Denominator polynomial coefficients.\n\n    See Also\n    --------\n    residue, invresz, unique_roots\n\n    "
    extra = k
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
    for k in range(len(pout)):
        temp = []
        for l in range(len(pout)):
            if (l != k):
                temp.extend(([pout[l]] * mult[l]))
        for m in range(mult[k]):
            t2 = temp[:]
            t2.extend(([pout[k]] * ((mult[k] - m) - 1)))
            b = np.polyadd(b, (r[indx] * np.atleast_1d(np.poly(t2))))
            indx += 1
    b = np.real_if_close(b)
    while (np.allclose(b[0], 0, rtol=1e-14) and (b.shape[(- 1)] > 1)):
        b = b[1:]
    return (b, a)