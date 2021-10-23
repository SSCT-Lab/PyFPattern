def test_linprog_cyclic_bland_bug_8561(self):
    c = np.array([7, 0, (- 4), 1.5, 1.5])
    A_ub = np.array([[4, 5.5, 1.5, 1.0, (- 3.5)], [1, (- 2.5), (- 2), 2.5, 0.5], [3, (- 0.5), 4, (- 12.5), (- 7)], [(- 1), 4.5, 2, (- 3.5), (- 2)], [5.5, 2, (- 4.5), (- 1), 9.5]])
    b_ub = np.array([0, 0, 0, 0, 1])
    if (self.method == 'simplex'):
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, options=dict(maxiter=100, bland=True), method=self.method)
    else:
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, options=dict(maxiter=100), method=self.method)
    _assert_success(res, desired_x=[0, 0, 19, (16 / 3), (29 / 3)])