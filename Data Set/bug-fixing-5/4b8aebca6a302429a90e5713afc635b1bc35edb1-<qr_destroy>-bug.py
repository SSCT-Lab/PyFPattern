def qr_destroy(la):
    '\n    Return QR decomposition of `la[0]`. Content of `la` gets destroyed in the process.\n\n    Using this function should be less memory intense than calling `scipy.linalg.qr(la[0])`,\n    because the memory used in `la[0]` is reclaimed earlier.\n    '
    a = np.asfortranarray(la[0])
    del la[0], la
    (m, n) = a.shape
    logger.debug('computing QR of %s dense matrix', str(a.shape))
    (geqrf,) = get_lapack_funcs(('geqrf',), (a,))
    (qr, tau, work, info) = geqrf(a, lwork=(- 1), overwrite_a=True)
    (qr, tau, work, info) = geqrf(a, lwork=work[0], overwrite_a=True)
    del a
    assert (info >= 0)
    r = triu(qr[:n, :n])
    if (m < n):
        qr = qr[:, :m]
    (gorgqr,) = get_lapack_funcs(('orgqr',), (qr,))
    (q, work, info) = gorgqr(qr, tau, lwork=(- 1), overwrite_a=True)
    (q, work, info) = gorgqr(qr, tau, lwork=work[0], overwrite_a=True)
    assert (info >= 0), 'qr failed'
    assert q.flags.f_contiguous
    return (q, r)