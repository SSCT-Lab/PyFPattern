

def _check_gen_eig(self, A, B):
    if (B is not None):
        (A, B) = (asarray(A), asarray(B))
        B0 = B
    else:
        A = asarray(A)
        B0 = B
        B = np.eye(*A.shape)
    msg = ('\n%r\n%r' % (A, B))
    (w, vr) = eig(A, B0, homogeneous_eigvals=True)
    wt = eigvals(A, B0, homogeneous_eigvals=True)
    val1 = (dot(A, vr) * w[1, :])
    val2 = (dot(B, vr) * w[0, :])
    for i in range(val1.shape[1]):
        assert_allclose(val1[:, i], val2[:, i], rtol=1e-13, atol=1e-13, err_msg=msg)
    if (B0 is None):
        assert_allclose(w[1, :], 1)
        assert_allclose(wt[1, :], 1)
    perm = np.lexsort(w)
    permt = np.lexsort(wt)
    assert_allclose(w[:, perm], wt[:, permt], err_msg=msg)
    length = np.empty(len(vr))
    for i in xrange(len(vr)):
        length[i] = norm(vr[:, i])
    assert_allclose(length, np.ones(length.size), err_msg=msg, atol=1e-07, rtol=1e-07)
    beta_nonzero = (w[1, :] != 0)
    wh = (w[(0, beta_nonzero)] / w[(1, beta_nonzero)])
    (w, vr) = eig(A, B0)
    wt = eigvals(A, B0)
    val1 = dot(A, vr)
    val2 = (dot(B, vr) * w)
    res = (val1 - val2)
    for i in range(res.shape[1]):
        if all(isfinite(res[:, i])):
            assert_allclose(res[:, i], 0, rtol=1e-13, atol=1e-13, err_msg=msg)
    assert_allclose(sort(w[isfinite(w)]), sort(wt[isfinite(wt)]), err_msg=msg)
    length = np.empty(len(vr))
    for i in xrange(len(vr)):
        length[i] = norm(vr[:, i])
    assert_allclose(length, np.ones(length.size), err_msg=msg)
    assert_allclose(sort(wh), sort(w[np.isfinite(w)]))
