def test_bounds_equal_but_infeasible2(self):
    c = [(- 4), 1]
    A_eq = [[7, (- 2)], [0, 1], [2, (- 2)]]
    b_eq = [14, 0, 3]
    bounds = [(2, 2), (0, None)]
    res = linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method=self.method, options=self.options)
    _assert_infeasible(res)