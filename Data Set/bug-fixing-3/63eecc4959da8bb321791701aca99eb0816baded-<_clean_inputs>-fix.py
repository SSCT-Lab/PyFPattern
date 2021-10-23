def _clean_inputs(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, x0=None):
    '\n    Given user inputs for a linear programming problem, return the\n    objective vector, upper bound constraints, equality constraints,\n    and simple bounds in a preferred format.\n\n    Parameters\n    ----------\n    c : 1D array\n        Coefficients of the linear objective function to be minimized.\n    A_ub : 2D array, optional\n        2D array such that ``A_ub @ x`` gives the values of the upper-bound\n        inequality constraints at ``x``.\n    b_ub : 1D array, optional\n        1D array of values representing the upper-bound of each inequality\n        constraint (row) in ``A_ub``.\n    A_eq : 2D array, optional\n        2D array such that ``A_eq @ x`` gives the values of the equality\n        constraints at ``x``.\n    b_eq : 1D array, optional\n        1D array of values representing the RHS of each equality constraint\n        (row) in ``A_eq``.\n    bounds : sequence, optional\n        ``(min, max)`` pairs for each element in ``x``, defining\n        the bounds on that parameter. Use None for one of ``min`` or\n        ``max`` when there is no bound in that direction. By default\n        bounds are ``(0, None)`` (non-negative).\n        If a sequence containing a single tuple is provided, then ``min`` and\n        ``max`` will be applied to all variables in the problem.\n    x0 : 1D array, optional\n        Starting values of the independent variables, which will be refined by\n        the optimization algorithm.\n\n    Returns\n    -------\n    c : 1D array\n        Coefficients of the linear objective function to be minimized.\n    A_ub : 2D array, optional\n        2D array such that ``A_ub @ x`` gives the values of the upper-bound\n        inequality constraints at ``x``.\n    b_ub : 1D array, optional\n        1D array of values representing the upper-bound of each inequality\n        constraint (row) in ``A_ub``.\n    A_eq : 2D array, optional\n        2D array such that ``A_eq @ x`` gives the values of the equality\n        constraints at ``x``.\n    b_eq : 1D array, optional\n        1D array of values representing the RHS of each equality constraint\n        (row) in ``A_eq``.\n    bounds : sequence of tuples\n        ``(min, max)`` pairs for each element in ``x``, defining\n        the bounds on that parameter. Use None for each of ``min`` or\n        ``max`` when there is no bound in that direction. By default\n        bounds are ``(0, None)`` (non-negative).\n    x0 : 1D array, optional\n        Starting values of the independent variables, which will be refined by\n        the optimization algorithm.\n    '
    if (c is None):
        raise TypeError
    try:
        c = np.array(c, dtype=np.float, copy=True).squeeze()
    except ValueError:
        raise TypeError('Invalid input for linprog: c must be a 1D array of numerical coefficients')
    else:
        if (c.size == 1):
            c = c.reshape((- 1))
        n_x = len(c)
        if ((n_x == 0) or (len(c.shape) != 1)):
            raise ValueError('Invalid input for linprog: c must be a 1D array and must not have more than one non-singleton dimension')
        if (not np.isfinite(c).all()):
            raise ValueError('Invalid input for linprog: c must not contain values inf, nan, or None')
    sparse_lhs = (sps.issparse(A_eq) or sps.issparse(A_ub))
    try:
        A_ub = _format_A_constraints(A_ub, n_x, sparse_lhs=sparse_lhs)
    except ValueError:
        raise TypeError('Invalid input for linprog: A_ub must be a 2D array of numerical values')
    else:
        n_ub = A_ub.shape[0]
        if ((len(A_ub.shape) != 2) or (A_ub.shape[1] != n_x)):
            raise ValueError('Invalid input for linprog: A_ub must have exactly two dimensions, and the number of columns in A_ub must be equal to the size of c')
        if ((sps.issparse(A_ub) and (not np.isfinite(A_ub.data).all())) or ((not sps.issparse(A_ub)) and (not np.isfinite(A_ub).all()))):
            raise ValueError('Invalid input for linprog: A_ub must not contain values inf, nan, or None')
    try:
        b_ub = _format_b_constraints(b_ub)
    except ValueError:
        raise TypeError('Invalid input for linprog: b_ub must be a 1D array of numerical values, each representing the upper bound of an inequality constraint (row) in A_ub')
    else:
        if (b_ub.shape != (n_ub,)):
            raise ValueError('Invalid input for linprog: b_ub must be a 1D array; b_ub must not have more than one non-singleton dimension and the number of rows in A_ub must equal the number of values in b_ub')
        if (not np.isfinite(b_ub).all()):
            raise ValueError('Invalid input for linprog: b_ub must not contain values inf, nan, or None')
    try:
        A_eq = _format_A_constraints(A_eq, n_x, sparse_lhs=sparse_lhs)
    except ValueError:
        raise TypeError('Invalid input for linprog: A_eq must be a 2D array of numerical values')
    else:
        n_eq = A_eq.shape[0]
        if ((len(A_eq.shape) != 2) or (A_eq.shape[1] != n_x)):
            raise ValueError('Invalid input for linprog: A_eq must have exactly two dimensions, and the number of columns in A_eq must be equal to the size of c')
        if ((sps.issparse(A_eq) and (not np.isfinite(A_eq.data).all())) or ((not sps.issparse(A_eq)) and (not np.isfinite(A_eq).all()))):
            raise ValueError('Invalid input for linprog: A_eq must not contain values inf, nan, or None')
    try:
        b_eq = _format_b_constraints(b_eq)
    except ValueError:
        raise TypeError('Invalid input for linprog: b_eq must be a 1D array of numerical values, each representing the upper bound of an inequality constraint (row) in A_eq')
    else:
        if (b_eq.shape != (n_eq,)):
            raise ValueError('Invalid input for linprog: b_eq must be a 1D array; b_eq must not have more than one non-singleton dimension and the number of rows in A_eq must equal the number of values in b_eq')
        if (not np.isfinite(b_eq).all()):
            raise ValueError('Invalid input for linprog: b_eq must not contain values inf, nan, or None')
    if (x0 is not None):
        try:
            x0 = np.array(x0, dtype=float, copy=True).squeeze()
        except ValueError:
            raise TypeError('Invalid input for linprog: x0 must be a 1D array of numerical coefficients')
        if (x0.ndim == 0):
            x0 = x0.reshape((- 1))
        if ((len(x0) == 0) or (x0.ndim != 1)):
            raise ValueError('Invalid input for linprog: x0 should be a 1D array; it must not have more than one non-singleton dimension')
        if (not (x0.size == c.size)):
            raise ValueError('Invalid input for linprog: x0 and c should contain the same number of elements')
        if (not np.isfinite(x0).all()):
            raise ValueError('Invalid input for linprog: x0 must not contain values inf, nan, or None')
    try:
        if isinstance(bounds, str):
            raise TypeError
        if ((bounds is None) or (len(bounds) == 0)):
            bounds = ([(0, None)] * n_x)
        elif (len(bounds) == 1):
            b = bounds[0]
            if (len(b) != 2):
                raise ValueError('Invalid input for linprog: exactly one lower bound and one upper bound must be specified for each element of x')
            bounds = ([b] * n_x)
        elif (len(bounds) == n_x):
            try:
                len(bounds[0])
            except BaseException:
                bounds = ([(bounds[0], bounds[1])] * n_x)
            for (i, b) in enumerate(bounds):
                if (len(b) != 2):
                    raise ValueError((((('Invalid input for linprog, bound ' + str(i)) + ' ') + str(b)) + ': exactly one lower bound and one upper bound must be specified for each element of x'))
        elif ((len(bounds) == 2) and np.isreal(bounds[0]) and np.isreal(bounds[1])):
            bounds = ([(bounds[0], bounds[1])] * n_x)
        else:
            raise ValueError('Invalid input for linprog: exactly one lower bound and one upper bound must be specified for each element of x')
        clean_bounds = []
        for (i, b) in enumerate(bounds):
            if ((b[0] is not None) and (b[1] is not None) and (b[0] > b[1])):
                raise ValueError((((('Invalid input for linprog, bound ' + str(i)) + ' ') + str(b)) + ': a lower bound must be less than or equal to the corresponding upper bound'))
            if (b[0] == np.inf):
                raise ValueError((((('Invalid input for linprog, bound ' + str(i)) + ' ') + str(b)) + ': infinity is not a valid lower bound'))
            if (b[1] == (- np.inf)):
                raise ValueError((((('Invalid input for linprog, bound ' + str(i)) + ' ') + str(b)) + ': negative infinity is not a valid upper bound'))
            lb = (float(b[0]) if ((b[0] is not None) and (b[0] != (- np.inf))) else None)
            ub = (float(b[1]) if ((b[1] is not None) and (b[1] != np.inf)) else None)
            clean_bounds.append((lb, ub))
        bounds = clean_bounds
    except ValueError as e:
        if ('could not convert string to float' in e.args[0]):
            raise TypeError
        else:
            raise e
    except TypeError as e:
        print(e)
        raise TypeError('Invalid input for linprog: bounds must be a sequence of (min,max) pairs, each defining bounds on an element of x ')
    return (c, A_ub, b_ub, A_eq, b_eq, bounds, x0)