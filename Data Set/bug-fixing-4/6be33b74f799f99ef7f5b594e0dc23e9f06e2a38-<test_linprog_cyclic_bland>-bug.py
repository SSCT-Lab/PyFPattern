def test_linprog_cyclic_bland(self):
    c = np.array([(- 10), 57, 9, 24.0])
    A_ub = np.array([[0.5, (- 5.5), (- 2.5), 9], [0.5, (- 1.5), (- 0.5), 1], [1, 0, 0, 0]])
    b_ub = [0, 0, 1]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, options=dict(maxiter=100), method=self.method)
    if (self.method == 'simplex'):
        assert_((not res.success))
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, options=dict(maxiter=100, bland=True), method=self.method)
    _assert_success(res, desired_x=[1, 0, 1, 0])