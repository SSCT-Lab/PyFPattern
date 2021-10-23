def _minimize_slsqp(func, x0, args=(), jac=None, bounds=None, constraints=(), maxiter=100, ftol=1e-06, iprint=1, disp=False, eps=_epsilon, callback=None, **unknown_options):
    '\n    Minimize a scalar function of one or more variables using Sequential\n    Least SQuares Programming (SLSQP).\n\n    Options\n    -------\n    ftol : float\n        Precision goal for the value of f in the stopping criterion.\n    eps : float\n        Step size used for numerical approximation of the jacobian.\n    disp : bool\n        Set to True to print convergence messages. If False,\n        `verbosity` is ignored and set to 0.\n    maxiter : int\n        Maximum number of iterations.\n\n    '
    _check_unknown_options(unknown_options)
    fprime = jac
    iter = maxiter
    acc = ftol
    epsilon = eps
    if (not disp):
        iprint = 0
    if isinstance(constraints, dict):
        constraints = (constraints,)
    cons = {
        'eq': (),
        'ineq': (),
    }
    for (ic, con) in enumerate(constraints):
        try:
            ctype = con['type'].lower()
        except KeyError:
            raise KeyError(('Constraint %d has no type defined.' % ic))
        except TypeError:
            raise TypeError('Constraints must be defined using a dictionary.')
        except AttributeError:
            raise TypeError("Constraint's type must be a string.")
        else:
            if (ctype not in ['eq', 'ineq']):
                raise ValueError(("Unknown constraint type '%s'." % con['type']))
        if ('fun' not in con):
            raise ValueError(('Constraint %d has no function defined.' % ic))
        cjac = con.get('jac')
        if (cjac is None):

            def cjac_factory(fun):

                def cjac(x, *args):
                    return approx_jacobian(x, fun, epsilon, *args)
                return cjac
            cjac = cjac_factory(con['fun'])
        cons[ctype] += ({
            'fun': con['fun'],
            'jac': cjac,
            'args': con.get('args', ()),
        },)
    exit_modes = {
        (- 1): 'Gradient evaluation required (g & a)',
        0: 'Optimization terminated successfully.',
        1: 'Function evaluation required (f & c)',
        2: 'More equality constraints than independent variables',
        3: 'More than 3*n iterations in LSQ subproblem',
        4: 'Inequality constraints incompatible',
        5: 'Singular matrix E in LSQ subproblem',
        6: 'Singular matrix C in LSQ subproblem',
        7: 'Rank-deficient equality constraint subproblem HFTI',
        8: 'Positive directional derivative for linesearch',
        9: 'Iteration limit exceeded',
    }
    (feval, func) = wrap_function(func, args)
    if fprime:
        (geval, fprime) = wrap_function(fprime, args)
    else:
        (geval, fprime) = wrap_function(approx_jacobian, (func, epsilon))
    x = asfarray(x0).flatten()
    meq = sum(map(len, [atleast_1d(c['fun'](x, *c['args'])) for c in cons['eq']]))
    mieq = sum(map(len, [atleast_1d(c['fun'](x, *c['args'])) for c in cons['ineq']]))
    m = (meq + mieq)
    la = array([1, m]).max()
    n = len(x)
    n1 = (n + 1)
    mineq = (((m - meq) + n1) + n1)
    len_w = (((((((((((((3 * n1) + m) * (n1 + 1)) + (((n1 - meq) + 1) * (mineq + 2))) + (2 * mineq)) + ((n1 + mineq) * (n1 - meq))) + (2 * meq)) + n1) + (((n + 1) * n) // 2)) + (2 * m)) + (3 * n)) + (3 * n1)) + 1)
    len_jw = mineq
    w = zeros(len_w)
    jw = zeros(len_jw)
    if ((bounds is None) or (len(bounds) == 0)):
        xl = np.empty(n, dtype=float)
        xu = np.empty(n, dtype=float)
        xl.fill(np.nan)
        xu.fill(np.nan)
    else:
        bnds = array(bounds, float)
        if (bnds.shape[0] != n):
            raise IndexError('SLSQP Error: the length of bounds is not compatible with that of x0.')
        bnderr = (bnds[:, 0] > bnds[:, 1])
        if bnderr.any():
            raise ValueError(('SLSQP Error: lb > ub in bounds %s.' % ', '.join((str(b) for b in bnderr))))
        (xl, xu) = (bnds[:, 0], bnds[:, 1])
        infbnd = (~ isfinite(bnds))
        xl[infbnd[:, 0]] = np.nan
        xu[infbnd[:, 1]] = np.nan
    mode = array(0, int)
    acc = array(acc, float)
    majiter = array(iter, int)
    majiter_prev = 0
    if (iprint >= 2):
        print(('%5s %5s %16s %16s' % ('NIT', 'FC', 'OBJFUN', 'GNORM')))
    while 1:
        if ((mode == 0) or (mode == 1)):
            try:
                fx = float(np.asarray(func(x)))
            except:
                raise ValueError('Objective function must return a scalar')
            if cons['eq']:
                c_eq = concatenate([atleast_1d(con['fun'](x, *con['args'])) for con in cons['eq']])
            else:
                c_eq = zeros(0)
            if cons['ineq']:
                c_ieq = concatenate([atleast_1d(con['fun'](x, *con['args'])) for con in cons['ineq']])
            else:
                c_ieq = zeros(0)
            c = concatenate((c_eq, c_ieq))
        if ((mode == 0) or (mode == (- 1))):
            g = append(fprime(x), 0.0)
            if cons['eq']:
                a_eq = vstack([con['jac'](x, *con['args']) for con in cons['eq']])
            else:
                a_eq = zeros((meq, n))
            if cons['ineq']:
                a_ieq = vstack([con['jac'](x, *con['args']) for con in cons['ineq']])
            else:
                a_ieq = zeros((mieq, n))
            if (m == 0):
                a = zeros((la, n))
            else:
                a = vstack((a_eq, a_ieq))
            a = concatenate((a, zeros([la, 1])), 1)
        slsqp(m, meq, x, xl, xu, fx, c, g, a, acc, majiter, mode, w, jw)
        if ((callback is not None) and (majiter > majiter_prev)):
            callback(x)
        if ((iprint >= 2) and (majiter > majiter_prev)):
            print(('%5i %5i % 16.6E % 16.6E' % (majiter, feval[0], fx, linalg.norm(g))))
        if (abs(mode) != 1):
            break
        majiter_prev = int(majiter)
    if (iprint >= 1):
        print((((exit_modes[int(mode)] + '    (Exit mode ') + str(mode)) + ')'))
        print('            Current function value:', fx)
        print('            Iterations:', majiter)
        print('            Function evaluations:', feval[0])
        print('            Gradient evaluations:', geval[0])
    return OptimizeResult(x=x, fun=fx, jac=g[:(- 1)], nit=int(majiter), nfev=feval[0], njev=geval[0], status=int(mode), message=exit_modes[int(mode)], success=(mode == 0))