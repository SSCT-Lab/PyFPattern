

def _linprog_simplex(c, c0, A, b, maxiter=1000, disp=False, callback=None, tol=1e-12, bland=False, _T_o=None, **unknown_options):
    '\n    Minimize a linear objective function subject to linear equality and\n    non-negativity constraints using the two phase simplex method.\n    Linear programming is intended to solve problems of the following form:\n\n    Minimize::\n\n        c @ x\n\n    Subject to::\n\n        A @ x == b\n            x >= 0\n\n    Parameters\n    ----------\n    c : 1D array\n        Coefficients of the linear objective function to be minimized.\n    c0 : float\n        Constant term in objective function due to fixed (and eliminated)\n        variables. (Purely for display.)\n    A : 2D array\n        2D array such that ``A @ x``, gives the values of the equality\n        constraints at ``x``.\n    b : 1D array\n        1D array of values representing the right hand side of each equality\n        constraint (row) in ``A``.\n    callback : callable, optional\n        If a callback function is provided, it will be called within each\n        iteration of the algorithm. The callback function must accept a single\n        `scipy.optimize.OptimizeResult` consisting of the following fields:\n\n            x : 1D array\n                Current solution vector\n            fun : float\n                Current value of the objective function\n            success : bool\n                True when an algorithm has completed successfully.\n            slack : 1D array\n                The values of the slack variables. Each slack variable\n                corresponds to an inequality constraint. If the slack is zero,\n                the corresponding constraint is active.\n            con : 1D array\n                The (nominally zero) residuals of the equality constraints,\n                that is, ``b - A_eq @ x``\n            phase : int\n                The phase of the algorithm being executed.\n            status : int\n                An integer representing the status of the optimization::\n\n                     0 : Algorithm proceeding nominally\n                     1 : Iteration limit reached\n                     2 : Problem appears to be infeasible\n                     3 : Problem appears to be unbounded\n                     4 : Serious numerical difficulties encountered\n            nit : int\n                The number of iterations performed.\n            message : str\n                A string descriptor of the exit status of the optimization.\n\n    Options\n    -------\n    maxiter : int\n       The maximum number of iterations to perform.\n    disp : bool\n        If True, print exit status message to sys.stdout\n    tol : float\n        The tolerance which determines when a solution is "close enough" to\n        zero in Phase 1 to be considered a basic feasible solution or close\n        enough to positive to serve as an optimal solution.\n    bland : bool\n        If True, use Bland\'s anti-cycling rule [3]_ to choose pivots to\n        prevent cycling. If False, choose pivots which should lead to a\n        converged solution more quickly. The latter method is subject to\n        cycling (non-convergence) in rare instances.\n\n    Returns\n    -------\n    x : 1D array\n        Solution vector.\n    status : int\n        An integer representing the exit status of the optimization::\n\n         0 : Optimization terminated successfully\n         1 : Iteration limit reached\n         2 : Problem appears to be infeasible\n         3 : Problem appears to be unbounded\n         4 : Serious numerical difficulties encountered\n\n    message : str\n        A string descriptor of the exit status of the optimization.\n    iteration : int\n        The number of iterations taken to solve the problem.\n\n    References\n    ----------\n    .. [1] Dantzig, George B., Linear programming and extensions. Rand\n           Corporation Research Study Princeton Univ. Press, Princeton, NJ,\n           1963\n    .. [2] Hillier, S.H. and Lieberman, G.J. (1995), "Introduction to\n           Mathematical Programming", McGraw-Hill, Chapter 4.\n    .. [3] Bland, Robert G. New finite pivoting rules for the simplex method.\n           Mathematics of Operations Research (2), 1977: pp. 103-107.\n\n\n    Notes\n    -----\n    The expected problem formulation differs between the top level ``linprog``\n    module and the method specific solvers. The method specific solvers expect a\n    problem in standard form:\n\n    Minimize::\n\n        c @ x\n\n    Subject to::\n\n        A @ x == b\n            x >= 0\n\n    Whereas the top level ``linprog`` module expects a problem of form:\n\n    Minimize::\n\n        c @ x\n\n    Subject to::\n\n        A_ub @ x <= b_ub\n        A_eq @ x == b_eq\n         lb <= x <= ub\n\n    where ``lb = 0`` and ``ub = None`` unless set in ``bounds``.\n\n    The original problem contains equality, upper-bound and variable constraints\n    whereas the method specific solver requires equality constraints and\n    variable non-negativity.\n\n    ``linprog`` module converts the original problem to standard form by\n    converting the simple bounds to upper bound constraints, introducing\n    non-negative slack variables for inequality constraints, and expressing\n    unbounded variables as the difference between two non-negative variables.\n    '
    _check_unknown_options(unknown_options)
    status = 0
    messages = {
        0: 'Optimization terminated successfully.',
        1: 'Iteration limit reached.',
        2: 'Optimization failed. Unable to find a feasible starting point.',
        3: 'Optimization failed. The problem appears to be unbounded.',
        4: 'Optimization failed. Singular matrix encountered.',
    }
    (n, m) = A.shape
    is_negative_constraint = np.less(b, 0)
    A[is_negative_constraint] *= (- 1)
    b[is_negative_constraint] *= (- 1)
    av = (np.arange(n) + m)
    basis = av.copy()
    row_constraints = np.hstack((A, np.eye(n), b[:, np.newaxis]))
    row_objective = np.hstack((c, np.zeros(n), c0))
    row_pseudo_objective = (- row_constraints.sum(axis=0))
    row_pseudo_objective[av] = 0
    T = np.vstack((row_constraints, row_objective, row_pseudo_objective))
    (nit1, status) = _solve_simplex(T, n, basis, phase=1, callback=callback, maxiter=maxiter, tol=tol, bland=bland, _T_o=_T_o)
    if (abs(T[((- 1), (- 1))]) < tol):
        T = T[:(- 1), :]
        T = np.delete(T, av, 1)
    else:
        status = 2
        nit2 = nit1
        messages[status] = "Phase 1 of the simplex method failed to find a feasible solution. The pseudo-objective function evaluates to {0:.1e} which exceeds the required tolerance of {1} for a solution to be considered 'close enough' to zero to be a basic solution. Consider increasing the tolerance to be greater than {0:.1e}. If this tolerance is unacceptably  large the problem may be infeasible.".format(abs(T[((- 1), (- 1))]), tol)
    if (status == 0):
        (nit2, status) = _solve_simplex(T, n, basis, maxiter=maxiter, phase=2, callback=callback, tol=tol, nit0=nit1, bland=bland, _T_o=_T_o)
    solution = np.zeros((n + m))
    solution[basis[:n]] = T[:n, (- 1)]
    x = solution[:m]
    return (x, status, messages[status], int(nit2))
