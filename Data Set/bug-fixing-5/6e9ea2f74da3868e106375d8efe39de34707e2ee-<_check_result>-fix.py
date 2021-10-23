def _check_result(x, fun, status, slack, con, lb, ub, tol, message):
    '\n    Check the validity of the provided solution.\n\n    A valid (optimal) solution satisfies all bounds, all slack variables are\n    negative and all equality constraint residuals are strictly non-zero.\n    Further, the lower-bounds, upper-bounds, slack and residuals contain\n    no nan values.\n\n    Parameters\n    ----------\n    x : 1D array\n        Solution vector to original linear programming problem\n    fun: float\n        optimal objective value for original problem\n    status : int\n        An integer representing the exit status of the optimization::\n\n             0 : Optimization terminated successfully\n             1 : Iteration limit reached\n             2 : Problem appears to be infeasible\n             3 : Problem appears to be unbounded\n             4 : Serious numerical difficulties encountered\n\n    slack : 1D array\n        The (non-negative) slack in the upper bound constraints, that is,\n        ``b_ub - A_ub @ x``\n    con : 1D array\n        The (nominally zero) residuals of the equality constraints, that is,\n        ``b - A_eq @ x``\n    lb : 1D array\n        The lower bound constraints on the original variables\n    ub: 1D array\n        The upper bound constraints on the original variables\n    message : str\n        A string descriptor of the exit status of the optimization.\n    tol : float\n        Termination tolerance; see [1]_ Section 4.5.\n\n    Returns\n    -------\n    status : int\n        An integer representing the exit status of the optimization::\n\n             0 : Optimization terminated successfully\n             1 : Iteration limit reached\n             2 : Problem appears to be infeasible\n             3 : Problem appears to be unbounded\n             4 : Serious numerical difficulties encountered\n\n    message : str\n        A string descriptor of the exit status of the optimization.\n    '
    tol = (np.sqrt(tol) * 10)
    contains_nans = (np.isnan(x).any() or np.isnan(fun) or np.isnan(slack).any() or np.isnan(con).any())
    if contains_nans:
        is_feasible = False
    else:
        invalid_bounds = ((x < (lb - tol)).any() or (x > (ub + tol)).any())
        invalid_slack = ((status != 3) and (slack < (- tol)).any())
        invalid_con = ((status != 3) and (np.abs(con) > tol).any())
        is_feasible = (not (invalid_bounds or invalid_slack or invalid_con))
    if ((status == 0) and (not is_feasible)):
        status = 4
        message = (('The solution does not satisfy the constraints within the required tolerance of ' + '{:.2E}'.format(tol)) + ', yet no errors were raised and there is no certificate of infeasibility or unboundedness. This is known to occur if the `presolve` option is False and the problem is infeasible. This can also occur due to the limited accuracy of the `interior-point` method. Check whether the slack and constraint residuals are acceptable; if not, consider enabling presolve, reducing option `tol`, and/or using method `revised simplex`. If you encounter this message under different circumstances, please submit a bug report.')
    elif ((status == 0) and contains_nans):
        status = 4
        message = "Numerical difficulties were encountered but no errors were raised. This is known to occur if the 'presolve' option is False, 'sparse' is True, and A_eq includes redundant rows. If you encounter this under different circumstances, please submit a bug report. Otherwise, remove linearly dependent equations from your equality constraints or enable presolve."
    elif ((status == 2) and is_feasible):
        raise ValueError(message)
    return (status, message)