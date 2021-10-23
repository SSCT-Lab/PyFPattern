@pytest.mark.parametrize('solver', [gmres, qmr, pytest.param(lgmres, marks=pytest.mark.xfail((platform.machine() == 'ppc64le'), reason='fails on ppc64le')), pytest.param(cgs, marks=pytest.mark.xfail), pytest.param(bicg, marks=pytest.mark.xfail), pytest.param(bicgstab, marks=pytest.mark.xfail), pytest.param(gcrotmk, marks=pytest.mark.xfail)])
def test_maxiter_worsening(solver):
    A = np.array([[(- 0.1112795288033378), 0, 0, 0.16127952880333685], [0, ((- 0.13627952880333782) + 6.283185307179586j), 0, 0], [0, 0, ((- 0.13627952880333782) - 6.283185307179586j), 0], [0.1112795288033368, 0j, 0j, (- 0.16127952880333785)]])
    v = np.ones(4)
    best_error = np.inf
    tol = (7 if (platform.machine() == 'aarch64') else 5)
    for maxiter in range(1, 20):
        (x, info) = solver(A, v, maxiter=maxiter, tol=1e-08, atol=0)
        if (info == 0):
            assert_((np.linalg.norm((A.dot(x) - v)) <= (1e-08 * np.linalg.norm(v))))
        error = np.linalg.norm((A.dot(x) - v))
        best_error = min(best_error, error)
        assert_((error <= (tol * best_error)))