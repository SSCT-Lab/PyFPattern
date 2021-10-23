def minimize(fun, x0, args=(), method=None, jac=None, hess=None, hessp=None, bounds=None, constraints=(), tol=None, callback=None, options=None):
    "Minimization of scalar function of one or more variables.\n\n    In general, the optimization problems are of the form::\n\n        minimize f(x) subject to\n\n        g_i(x) >= 0,  i = 1,...,m\n        h_j(x)  = 0,  j = 1,...,p\n\n    where x is a vector of one or more variables.\n    ``g_i(x)`` are the inequality constraints.\n    ``h_j(x)`` are the equality constrains.\n\n    Optionally, the lower and upper bounds for each element in x can also be\n    specified using the `bounds` argument.\n\n    Parameters\n    ----------\n    fun : callable\n        Objective function.\n    x0 : ndarray\n        Initial guess.\n    args : tuple, optional\n        Extra arguments passed to the objective function and its\n        derivatives (Jacobian, Hessian).\n    method : str or callable, optional\n        Type of solver.  Should be one of\n\n            - 'Nelder-Mead' :ref:`(see here) <optimize.minimize-neldermead>`\n            - 'Powell'      :ref:`(see here) <optimize.minimize-powell>`\n            - 'CG'          :ref:`(see here) <optimize.minimize-cg>`\n            - 'BFGS'        :ref:`(see here) <optimize.minimize-bfgs>`\n            - 'Newton-CG'   :ref:`(see here) <optimize.minimize-newtoncg>`\n            - 'L-BFGS-B'    :ref:`(see here) <optimize.minimize-lbfgsb>`\n            - 'TNC'         :ref:`(see here) <optimize.minimize-tnc>`\n            - 'COBYLA'      :ref:`(see here) <optimize.minimize-cobyla>`\n            - 'SLSQP'       :ref:`(see here) <optimize.minimize-slsqp>`\n            - 'dogleg'      :ref:`(see here) <optimize.minimize-dogleg>`\n            - 'trust-ncg'   :ref:`(see here) <optimize.minimize-trustncg>`\n            - 'trust-exact' :ref:`(see here) <optimize.minimize-trustexact>`\n            - custom - a callable object (added in version 0.14.0),\n              see below for description.\n\n        If not given, chosen to be one of ``BFGS``, ``L-BFGS-B``, ``SLSQP``,\n        depending if the problem has constraints or bounds.\n    jac : bool or callable, optional\n        Jacobian (gradient) of objective function. Only for CG, BFGS,\n        Newton-CG, L-BFGS-B, TNC, SLSQP, dogleg, trust-ncg.\n        If `jac` is a Boolean and is True, `fun` is assumed to return the\n        gradient along with the objective function. If False, the\n        gradient will be estimated numerically.\n        `jac` can also be a callable returning the gradient of the\n        objective. In this case, it must accept the same arguments as `fun`.\n    hess, hessp : callable, optional\n        Hessian (matrix of second-order derivatives) of objective function or\n        Hessian of objective function times an arbitrary vector p.  Only for\n        Newton-CG, dogleg, trust-ncg.\n        Only one of `hessp` or `hess` needs to be given.  If `hess` is\n        provided, then `hessp` will be ignored.  If neither `hess` nor\n        `hessp` is provided, then the Hessian product will be approximated\n        using finite differences on `jac`. `hessp` must compute the Hessian\n        times an arbitrary vector.\n    bounds : sequence, optional\n        Bounds for variables (only for L-BFGS-B, TNC and SLSQP).\n        ``(min, max)`` pairs for each element in ``x``, defining\n        the bounds on that parameter. Use None for one of ``min`` or\n        ``max`` when there is no bound in that direction.\n    constraints : dict or sequence of dict, optional\n        Constraints definition (only for COBYLA and SLSQP).\n        Each constraint is defined in a dictionary with fields:\n\n            type : str\n                Constraint type: 'eq' for equality, 'ineq' for inequality.\n            fun : callable\n                The function defining the constraint.\n            jac : callable, optional\n                The Jacobian of `fun` (only for SLSQP).\n            args : sequence, optional\n                Extra arguments to be passed to the function and Jacobian.\n\n        Equality constraint means that the constraint function result is to\n        be zero whereas inequality means that it is to be non-negative.\n        Note that COBYLA only supports inequality constraints.\n    tol : float, optional\n        Tolerance for termination. For detailed control, use solver-specific\n        options.\n    options : dict, optional\n        A dictionary of solver options. All methods accept the following\n        generic options:\n\n            maxiter : int\n                Maximum number of iterations to perform.\n            disp : bool\n                Set to True to print convergence messages.\n\n        For method-specific options, see :func:`show_options()`.\n    callback : callable, optional\n        Called after each iteration, as ``callback(xk)``, where ``xk`` is the\n        current parameter vector.\n\n    Returns\n    -------\n    res : OptimizeResult\n        The optimization result represented as a ``OptimizeResult`` object.\n        Important attributes are: ``x`` the solution array, ``success`` a\n        Boolean flag indicating if the optimizer exited successfully and\n        ``message`` which describes the cause of the termination. See\n        `OptimizeResult` for a description of other attributes.\n\n\n    See also\n    --------\n    minimize_scalar : Interface to minimization algorithms for scalar\n        univariate functions\n    show_options : Additional options accepted by the solvers\n\n    Notes\n    -----\n    This section describes the available solvers that can be selected by the\n    'method' parameter. The default method is *BFGS*.\n\n    **Unconstrained minimization**\n\n    Method :ref:`Nelder-Mead <optimize.minimize-neldermead>` uses the\n    Simplex algorithm [1]_, [2]_. This algorithm is robust in many\n    applications. However, if numerical computation of derivative can be\n    trusted, other algorithms using the first and/or second derivatives\n    information might be preferred for their better performance in\n    general.\n\n    Method :ref:`Powell <optimize.minimize-powell>` is a modification\n    of Powell's method [3]_, [4]_ which is a conjugate direction\n    method. It performs sequential one-dimensional minimizations along\n    each vector of the directions set (`direc` field in `options` and\n    `info`), which is updated at each iteration of the main\n    minimization loop. The function need not be differentiable, and no\n    derivatives are taken.\n\n    Method :ref:`CG <optimize.minimize-cg>` uses a nonlinear conjugate\n    gradient algorithm by Polak and Ribiere, a variant of the\n    Fletcher-Reeves method described in [5]_ pp.  120-122. Only the\n    first derivatives are used.\n\n    Method :ref:`BFGS <optimize.minimize-bfgs>` uses the quasi-Newton\n    method of Broyden, Fletcher, Goldfarb, and Shanno (BFGS) [5]_\n    pp. 136. It uses the first derivatives only. BFGS has proven good\n    performance even for non-smooth optimizations. This method also\n    returns an approximation of the Hessian inverse, stored as\n    `hess_inv` in the OptimizeResult object.\n\n    Method :ref:`Newton-CG <optimize.minimize-newtoncg>` uses a\n    Newton-CG algorithm [5]_ pp. 168 (also known as the truncated\n    Newton method). It uses a CG method to the compute the search\n    direction. See also *TNC* method for a box-constrained\n    minimization with a similar algorithm. Suitable for large-scale\n    problems.\n\n    Method :ref:`dogleg <optimize.minimize-dogleg>` uses the dog-leg\n    trust-region algorithm [5]_ for unconstrained minimization. This\n    algorithm requires the gradient and Hessian; furthermore the\n    Hessian is required to be positive definite.\n\n    Method :ref:`trust-ncg <optimize.minimize-trustncg>` uses the\n    Newton conjugate gradient trust-region algorithm [5]_ for\n    unconstrained minimization. This algorithm requires the gradient\n    and either the Hessian or a function that computes the product of\n    the Hessian with a given vector. Suitable for large-scale problems.\n\n    Method :ref:`trust-exact <optimize.minimize-trustexact>`\n    is a trust-region method for unconstrained minimization in which\n    quadratic subproblems are solved almost exactly [13]_. This\n    algorithm requires the gradient and the Hessian (which is\n    *not* required to be positive definite). It is, in many\n    situations, the Newton method to converge in fewer iteraction\n    and the most recommended for small and medium-size problems.\n\n    **Constrained minimization**\n\n    Method :ref:`L-BFGS-B <optimize.minimize-lbfgsb>` uses the L-BFGS-B\n    algorithm [6]_, [7]_ for bound constrained minimization.\n\n    Method :ref:`TNC <optimize.minimize-tnc>` uses a truncated Newton\n    algorithm [5]_, [8]_ to minimize a function with variables subject\n    to bounds. This algorithm uses gradient information; it is also\n    called Newton Conjugate-Gradient. It differs from the *Newton-CG*\n    method described above as it wraps a C implementation and allows\n    each variable to be given upper and lower bounds.\n\n    Method :ref:`COBYLA <optimize.minimize-cobyla>` uses the\n    Constrained Optimization BY Linear Approximation (COBYLA) method\n    [9]_, [10]_, [11]_. The algorithm is based on linear\n    approximations to the objective function and each constraint. The\n    method wraps a FORTRAN implementation of the algorithm. The\n    constraints functions 'fun' may return either a single number\n    or an array or list of numbers.\n\n    Method :ref:`SLSQP <optimize.minimize-slsqp>` uses Sequential\n    Least SQuares Programming to minimize a function of several\n    variables with any combination of bounds, equality and inequality\n    constraints. The method wraps the SLSQP Optimization subroutine\n    originally implemented by Dieter Kraft [12]_. Note that the\n    wrapper handles infinite values in bounds by converting them into\n    large floating values.\n\n    **Custom minimizers**\n\n    It may be useful to pass a custom minimization method, for example\n    when using a frontend to this method such as `scipy.optimize.basinhopping`\n    or a different library.  You can simply pass a callable as the ``method``\n    parameter.\n\n    The callable is called as ``method(fun, x0, args, **kwargs, **options)``\n    where ``kwargs`` corresponds to any other parameters passed to `minimize`\n    (such as `callback`, `hess`, etc.), except the `options` dict, which has\n    its contents also passed as `method` parameters pair by pair.  Also, if\n    `jac` has been passed as a bool type, `jac` and `fun` are mangled so that\n    `fun` returns just the function values and `jac` is converted to a function\n    returning the Jacobian.  The method shall return an ``OptimizeResult``\n    object.\n\n    The provided `method` callable must be able to accept (and possibly ignore)\n    arbitrary parameters; the set of parameters accepted by `minimize` may\n    expand in future versions and then these parameters will be passed to\n    the method.  You can find an example in the scipy.optimize tutorial.\n\n    .. versionadded:: 0.11.0\n\n    References\n    ----------\n    .. [1] Nelder, J A, and R Mead. 1965. A Simplex Method for Function\n        Minimization. The Computer Journal 7: 308-13.\n    .. [2] Wright M H. 1996. Direct search methods: Once scorned, now\n        respectable, in Numerical Analysis 1995: Proceedings of the 1995\n        Dundee Biennial Conference in Numerical Analysis (Eds. D F\n        Griffiths and G A Watson). Addison Wesley Longman, Harlow, UK.\n        191-208.\n    .. [3] Powell, M J D. 1964. An efficient method for finding the minimum of\n       a function of several variables without calculating derivatives. The\n       Computer Journal 7: 155-162.\n    .. [4] Press W, S A Teukolsky, W T Vetterling and B P Flannery.\n       Numerical Recipes (any edition), Cambridge University Press.\n    .. [5] Nocedal, J, and S J Wright. 2006. Numerical Optimization.\n       Springer New York.\n    .. [6] Byrd, R H and P Lu and J. Nocedal. 1995. A Limited Memory\n       Algorithm for Bound Constrained Optimization. SIAM Journal on\n       Scientific and Statistical Computing 16 (5): 1190-1208.\n    .. [7] Zhu, C and R H Byrd and J Nocedal. 1997. L-BFGS-B: Algorithm\n       778: L-BFGS-B, FORTRAN routines for large scale bound constrained\n       optimization. ACM Transactions on Mathematical Software 23 (4):\n       550-560.\n    .. [8] Nash, S G. Newton-Type Minimization Via the Lanczos Method.\n       1984. SIAM Journal of Numerical Analysis 21: 770-778.\n    .. [9] Powell, M J D. A direct search optimization method that models\n       the objective and constraint functions by linear interpolation.\n       1994. Advances in Optimization and Numerical Analysis, eds. S. Gomez\n       and J-P Hennart, Kluwer Academic (Dordrecht), 51-67.\n    .. [10] Powell M J D. Direct search algorithms for optimization\n       calculations. 1998. Acta Numerica 7: 287-336.\n    .. [11] Powell M J D. A view of algorithms for optimization without\n       derivatives. 2007.Cambridge University Technical Report DAMTP\n       2007/NA03\n    .. [12] Kraft, D. A software package for sequential quadratic\n       programming. 1988. Tech. Rep. DFVLR-FB 88-28, DLR German Aerospace\n       Center -- Institute for Flight Mechanics, Koln, Germany.\n    .. [13] Conn, A. R., Gould, N. I., and Toint, P. L.\n       Trust region methods. 2000. Siam. pp. 169-200.\n\n    Examples\n    --------\n    Let us consider the problem of minimizing the Rosenbrock function. This\n    function (and its respective derivatives) is implemented in `rosen`\n    (resp. `rosen_der`, `rosen_hess`) in the `scipy.optimize`.\n\n    >>> from scipy.optimize import minimize, rosen, rosen_der\n\n    A simple application of the *Nelder-Mead* method is:\n\n    >>> x0 = [1.3, 0.7, 0.8, 1.9, 1.2]\n    >>> res = minimize(rosen, x0, method='Nelder-Mead', tol=1e-6)\n    >>> res.x\n    array([ 1.,  1.,  1.,  1.,  1.])\n\n    Now using the *BFGS* algorithm, using the first derivative and a few\n    options:\n\n    >>> res = minimize(rosen, x0, method='BFGS', jac=rosen_der,\n    ...                options={'gtol': 1e-6, 'disp': True})\n    Optimization terminated successfully.\n             Current function value: 0.000000\n             Iterations: 33\n             Function evaluations: 35\n             Gradient evaluations: 35\n    >>> res.x\n    array([ 1.,  1.,  1.,  1.,  1.])\n    >>> print(res.message)\n    Optimization terminated successfully.\n    >>> res.hess_inv\n    array([[ 0.00749589,  0.01255155,  0.02396251,  0.04750988,  0.09495377],  # may vary\n           [ 0.01255155,  0.02510441,  0.04794055,  0.09502834,  0.18996269],\n           [ 0.02396251,  0.04794055,  0.09631614,  0.19092151,  0.38165151],\n           [ 0.04750988,  0.09502834,  0.19092151,  0.38341252,  0.7664427 ],\n           [ 0.09495377,  0.18996269,  0.38165151,  0.7664427,   1.53713523]])\n\n\n    Next, consider a minimization problem with several constraints (namely\n    Example 16.4 from [5]_). The objective function is:\n\n    >>> fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2\n\n    There are three constraints defined as:\n\n    >>> cons = ({'type': 'ineq', 'fun': lambda x:  x[0] - 2 * x[1] + 2},\n    ...         {'type': 'ineq', 'fun': lambda x: -x[0] - 2 * x[1] + 6},\n    ...         {'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] + 2})\n\n    And variables must be positive, hence the following bounds:\n\n    >>> bnds = ((0, None), (0, None))\n\n    The optimization problem is solved using the SLSQP method as:\n\n    >>> res = minimize(fun, (2, 0), method='SLSQP', bounds=bnds,\n    ...                constraints=cons)\n\n    It should converge to the theoretical solution (1.4 ,1.7).\n\n    "
    x0 = np.asarray(x0)
    if (x0.dtype.kind in np.typecodes['AllInteger']):
        x0 = np.asarray(x0, dtype=float)
    if (not isinstance(args, tuple)):
        args = (args,)
    if (method is None):
        if constraints:
            method = 'SLSQP'
        elif (bounds is not None):
            method = 'L-BFGS-B'
        else:
            method = 'BFGS'
    if callable(method):
        meth = '_custom'
    else:
        meth = method.lower()
    if (options is None):
        options = {
            
        }
    if ((meth in ['nelder-mead', 'powell', 'cobyla']) and bool(jac)):
        warn(('Method %s does not use gradient information (jac).' % method), RuntimeWarning)
    if ((meth not in ('newton-cg', 'dogleg', 'trust-ncg', 'trust-exact', '_custom')) and (hess is not None)):
        warn(('Method %s does not use Hessian information (hess).' % method), RuntimeWarning)
    if ((meth not in ('newton-cg', 'dogleg', 'trust-ncg', '_custom')) and (hessp is not None)):
        warn(('Method %s does not use Hessian-vector product information (hessp).' % method), RuntimeWarning)
    if ((meth in ['nelder-mead', 'powell', 'cg', 'bfgs', 'newton-cg', 'dogleg', 'trust-ncg']) and ((bounds is not None) or np.any(constraints))):
        warn(('Method %s cannot handle constraints nor bounds.' % method), RuntimeWarning)
    if ((meth in ['l-bfgs-b', 'tnc']) and np.any(constraints)):
        warn(('Method %s cannot handle constraints.' % method), RuntimeWarning)
    if ((meth == 'cobyla') and (bounds is not None)):
        warn(('Method %s cannot handle bounds.' % method), RuntimeWarning)
    if ((meth in ['cobyla']) and (callback is not None)):
        warn(('Method %s does not support callback.' % method), RuntimeWarning)
    if ((meth in ['l-bfgs-b', 'tnc', 'cobyla', 'slsqp']) and options.get('return_all', False)):
        warn(('Method %s does not support the return_all option.' % method), RuntimeWarning)
    if (not callable(jac)):
        if bool(jac):
            fun = MemoizeJac(fun)
            jac = fun.derivative
        else:
            jac = None
    if (tol is not None):
        options = dict(options)
        if (meth == 'nelder-mead'):
            options.setdefault('xatol', tol)
            options.setdefault('fatol', tol)
        if (meth in ['newton-cg', 'powell', 'tnc']):
            options.setdefault('xtol', tol)
        if (meth in ['powell', 'l-bfgs-b', 'tnc', 'slsqp']):
            options.setdefault('ftol', tol)
        if (meth in ['bfgs', 'cg', 'l-bfgs-b', 'tnc', 'dogleg', 'trust-ncg', 'trust-exact']):
            options.setdefault('gtol', tol)
        if (meth in ['cobyla', '_custom']):
            options.setdefault('tol', tol)
    if (meth == '_custom'):
        return method(fun, x0, args=args, jac=jac, hess=hess, hessp=hessp, bounds=bounds, constraints=constraints, callback=callback, **options)
    elif (meth == 'nelder-mead'):
        return _minimize_neldermead(fun, x0, args, callback, **options)
    elif (meth == 'powell'):
        return _minimize_powell(fun, x0, args, callback, **options)
    elif (meth == 'cg'):
        return _minimize_cg(fun, x0, args, jac, callback, **options)
    elif (meth == 'bfgs'):
        return _minimize_bfgs(fun, x0, args, jac, callback, **options)
    elif (meth == 'newton-cg'):
        return _minimize_newtoncg(fun, x0, args, jac, hess, hessp, callback, **options)
    elif (meth == 'l-bfgs-b'):
        return _minimize_lbfgsb(fun, x0, args, jac, bounds, callback=callback, **options)
    elif (meth == 'tnc'):
        return _minimize_tnc(fun, x0, args, jac, bounds, callback=callback, **options)
    elif (meth == 'cobyla'):
        return _minimize_cobyla(fun, x0, args, constraints, **options)
    elif (meth == 'slsqp'):
        return _minimize_slsqp(fun, x0, args, jac, bounds, constraints, callback=callback, **options)
    elif (meth == 'dogleg'):
        return _minimize_dogleg(fun, x0, args, jac, hess, callback=callback, **options)
    elif (meth == 'trust-ncg'):
        return _minimize_trust_ncg(fun, x0, args, jac, hess, hessp, callback=callback, **options)
    elif (meth == 'trust-exact'):
        return _minimize_trustregion_exact(fun, x0, args, jac, hess, callback=callback, **options)
    else:
        raise ValueError(('Unknown solver %s' % method))