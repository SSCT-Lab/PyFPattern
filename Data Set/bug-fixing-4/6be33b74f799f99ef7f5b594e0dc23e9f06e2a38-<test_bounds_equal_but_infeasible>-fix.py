def test_bounds_equal_but_infeasible(self):
    c = [(- 4), 1]
    A_ub = [[7, (- 2)], [0, 1], [2, (- 2)]]
    b_ub = [14, 0, 3]
    bounds = [(2, 2), (0, None)]
    res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=self.method, options=self.options)
    _assert_infeasible(res)