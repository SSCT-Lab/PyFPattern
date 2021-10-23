def test_bug_7044(self):
    (A, b, c, N) = magic_square(3)
    with suppress_warnings() as sup:
        sup.filter(OptimizeWarning, 'A_eq does not appear...')
        res = linprog(c, A_eq=A, b_eq=b, method=self.method, options=self.options)
    desired_fun = 1.730550597
    _assert_success(res, desired_fun=desired_fun)
    assert_allclose(A.dot(res.x), b)
    assert_array_less((np.zeros(res.x.size) - 1e-05), res.x)