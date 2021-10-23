def _qz(A, B, output='real', lwork=None, sort=None, overwrite_a=False, overwrite_b=False, check_finite=True):
    if (sort is not None):
        raise ValueError("The 'sort' input of qz() has to be None and will be removed in a future release. Use ordqz instead.")
    if (output not in ['real', 'complex', 'r', 'c']):
        raise ValueError("argument must be 'real', or 'complex'")
    if check_finite:
        a1 = asarray_chkfinite(A)
        b1 = asarray_chkfinite(B)
    else:
        a1 = np.asarray(A)
        b1 = np.asarray(B)
    (a_m, a_n) = a1.shape
    (b_m, b_n) = b1.shape
    if (not (a_m == a_n == b_m == b_n)):
        raise ValueError('Array dimensions must be square and agree')
    typa = a1.dtype.char
    if ((output in ['complex', 'c']) and (typa not in ['F', 'D'])):
        if (typa in _double_precision):
            a1 = a1.astype('D')
            typa = 'D'
        else:
            a1 = a1.astype('F')
            typa = 'F'
    typb = b1.dtype.char
    if ((output in ['complex', 'c']) and (typb not in ['F', 'D'])):
        if (typb in _double_precision):
            b1 = b1.astype('D')
            typb = 'D'
        else:
            b1 = b1.astype('F')
            typb = 'F'
    overwrite_a = (overwrite_a or _datacopied(a1, A))
    overwrite_b = (overwrite_b or _datacopied(b1, B))
    (gges,) = get_lapack_funcs(('gges',), (a1, b1))
    if ((lwork is None) or (lwork == (- 1))):
        result = gges((lambda x: None), a1, b1, lwork=(- 1))
        lwork = result[(- 2)][0].real.astype(np.int)
    sfunction = (lambda x: None)
    result = gges(sfunction, a1, b1, lwork=lwork, overwrite_a=overwrite_a, overwrite_b=overwrite_b, sort_t=0)
    info = result[(- 1)]
    if (info < 0):
        raise ValueError('Illegal value in argument {} of gges'.format((- info)))
    elif ((info > 0) and (info <= a_n)):
        warnings.warn('The QZ iteration failed. (a,b) are not in Schur form, but ALPHAR(j), ALPHAI(j), and BETA(j) should be correct for J={},...,N'.format((info - 1)), LinAlgWarning, stacklevel=3)
    elif (info == (a_n + 1)):
        raise LinAlgError('Something other than QZ iteration failed')
    elif (info == (a_n + 2)):
        raise LinAlgError('After reordering, roundoff changed values of some complex eigenvalues so that leading eigenvalues in the Generalized Schur form no longer satisfy sort=True. This could also be due to scaling.')
    elif (info == (a_n + 3)):
        raise LinAlgError('Reordering failed in <s,d,c,z>tgsen')
    return (result, gges.typecode)