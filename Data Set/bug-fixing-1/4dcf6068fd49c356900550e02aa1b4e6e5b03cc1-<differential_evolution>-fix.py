

def differential_evolution(func, bounds, args=(), strategy='best1bin', maxiter=1000, popsize=15, tol=0.01, mutation=(0.5, 1), recombination=0.7, seed=None, callback=None, disp=False, polish=True, init='latinhypercube', atol=0, updating='immediate', workers=1, constraints=()):
    "Finds the global minimum of a multivariate function.\n\n    Differential Evolution is stochastic in nature (does not use gradient\n    methods) to find the minimum, and can search large areas of candidate\n    space, but often requires larger numbers of function evaluations than\n    conventional gradient based techniques.\n\n    The algorithm is due to Storn and Price [1]_.\n\n    Parameters\n    ----------\n    func : callable\n        The objective function to be minimized.  Must be in the form\n        ``f(x, *args)``, where ``x`` is the argument in the form of a 1-D array\n        and ``args`` is a  tuple of any additional fixed parameters needed to\n        completely specify the function.\n    bounds : sequence or `Bounds`, optional\n        Bounds for variables.  There are two ways to specify the bounds:\n        1. Instance of `Bounds` class.\n        2. ``(min, max)`` pairs for each element in ``x``, defining the finite\n        lower and upper bounds for the optimizing argument of `func`. It is\n        required to have ``len(bounds) == len(x)``. ``len(bounds)`` is used\n        to determine the number of parameters in ``x``.\n    args : tuple, optional\n        Any additional fixed parameters needed to\n        completely specify the objective function.\n    strategy : str, optional\n        The differential evolution strategy to use. Should be one of:\n\n            - 'best1bin'\n            - 'best1exp'\n            - 'rand1exp'\n            - 'randtobest1exp'\n            - 'currenttobest1exp'\n            - 'best2exp'\n            - 'rand2exp'\n            - 'randtobest1bin'\n            - 'currenttobest1bin'\n            - 'best2bin'\n            - 'rand2bin'\n            - 'rand1bin'\n\n        The default is 'best1bin'.\n    maxiter : int, optional\n        The maximum number of generations over which the entire population is\n        evolved. The maximum number of function evaluations (with no polishing)\n        is: ``(maxiter + 1) * popsize * len(x)``\n    popsize : int, optional\n        A multiplier for setting the total population size.  The population has\n        ``popsize * len(x)`` individuals (unless the initial population is\n        supplied via the `init` keyword).\n    tol : float, optional\n        Relative tolerance for convergence, the solving stops when\n        ``np.std(pop) <= atol + tol * np.abs(np.mean(population_energies))``,\n        where and `atol` and `tol` are the absolute and relative tolerance\n        respectively.\n    mutation : float or tuple(float, float), optional\n        The mutation constant. In the literature this is also known as\n        differential weight, being denoted by F.\n        If specified as a float it should be in the range [0, 2].\n        If specified as a tuple ``(min, max)`` dithering is employed. Dithering\n        randomly changes the mutation constant on a generation by generation\n        basis. The mutation constant for that generation is taken from\n        ``U[min, max)``. Dithering can help speed convergence significantly.\n        Increasing the mutation constant increases the search radius, but will\n        slow down convergence.\n    recombination : float, optional\n        The recombination constant, should be in the range [0, 1]. In the\n        literature this is also known as the crossover probability, being\n        denoted by CR. Increasing this value allows a larger number of mutants\n        to progress into the next generation, but at the risk of population\n        stability.\n    seed : int or `np.random.RandomState`, optional\n        If `seed` is not specified the `np.RandomState` singleton is used.\n        If `seed` is an int, a new `np.random.RandomState` instance is used,\n        seeded with seed.\n        If `seed` is already a `np.random.RandomState instance`, then that\n        `np.random.RandomState` instance is used.\n        Specify `seed` for repeatable minimizations.\n    disp : bool, optional\n        Prints the evaluated `func` at every iteration.\n    callback : callable, `callback(xk, convergence=val)`, optional\n        A function to follow the progress of the minimization. ``xk`` is\n        the current value of ``x0``. ``val`` represents the fractional\n        value of the population convergence.  When ``val`` is greater than one\n        the function halts. If callback returns `True`, then the minimization\n        is halted (any polishing is still carried out).\n    polish : bool, optional\n        If True (default), then `scipy.optimize.minimize` with the `L-BFGS-B`\n        method is used to polish the best population member at the end, which\n        can improve the minimization slightly. If a constrained problem is\n        being studied then the `trust-constr` method is used instead.\n    init : str or array-like, optional\n        Specify which type of population initialization is performed. Should be\n        one of:\n\n            - 'latinhypercube'\n            - 'random'\n            - array specifying the initial population. The array should have\n              shape ``(M, len(x))``, where len(x) is the number of parameters.\n              `init` is clipped to `bounds` before use.\n\n        The default is 'latinhypercube'. Latin Hypercube sampling tries to\n        maximize coverage of the available parameter space. 'random'\n        initializes the population randomly - this has the drawback that\n        clustering can occur, preventing the whole of parameter space being\n        covered. Use of an array to specify a population subset could be used,\n        for example, to create a tight bunch of initial guesses in an location\n        where the solution is known to exist, thereby reducing time for\n        convergence.\n    atol : float, optional\n        Absolute tolerance for convergence, the solving stops when\n        ``np.std(pop) <= atol + tol * np.abs(np.mean(population_energies))``,\n        where and `atol` and `tol` are the absolute and relative tolerance\n        respectively.\n    updating : {'immediate', 'deferred'}, optional\n        If ``'immediate'``, the best solution vector is continuously updated\n        within a single generation [4]_. This can lead to faster convergence as\n        trial vectors can take advantage of continuous improvements in the best\n        solution.\n        With ``'deferred'``, the best solution vector is updated once per\n        generation. Only ``'deferred'`` is compatible with parallelization, and\n        the `workers` keyword can over-ride this option.\n\n        .. versionadded:: 1.2.0\n\n    workers : int or map-like callable, optional\n        If `workers` is an int the population is subdivided into `workers`\n        sections and evaluated in parallel\n        (uses `multiprocessing.Pool <multiprocessing>`).\n        Supply -1 to use all available CPU cores.\n        Alternatively supply a map-like callable, such as\n        `multiprocessing.Pool.map` for evaluating the population in parallel.\n        This evaluation is carried out as ``workers(func, iterable)``.\n        This option will override the `updating` keyword to\n        ``updating='deferred'`` if ``workers != 1``.\n        Requires that `func` be pickleable.\n\n        .. versionadded:: 1.2.0\n\n    constraints : {NonLinearConstraint, LinearConstraint, Bounds}\n        Constraints on the solver, over and above those applied by the `bounds`\n        kwd. Uses the approach by Lampinen [5]_.\n\n        .. versionadded:: 1.4.0\n\n    Returns\n    -------\n    res : OptimizeResult\n        The optimization result represented as a `OptimizeResult` object.\n        Important attributes are: ``x`` the solution array, ``success`` a\n        Boolean flag indicating if the optimizer exited successfully and\n        ``message`` which describes the cause of the termination. See\n        `OptimizeResult` for a description of other attributes.  If `polish`\n        was employed, and a lower minimum was obtained by the polishing, then\n        OptimizeResult also contains the ``jac`` attribute.\n        If the eventual solution does not satisfy the applied constraints\n        ``success`` will be `False`.\n\n    Notes\n    -----\n    Differential evolution is a stochastic population based method that is\n    useful for global optimization problems. At each pass through the population\n    the algorithm mutates each candidate solution by mixing with other candidate\n    solutions to create a trial candidate. There are several strategies [2]_ for\n    creating trial candidates, which suit some problems more than others. The\n    'best1bin' strategy is a good starting point for many systems. In this\n    strategy two members of the population are randomly chosen. Their difference\n    is used to mutate the best member (the `best` in `best1bin`), :math:`b_0`,\n    so far:\n\n    .. math::\n\n        b' = b_0 + mutation * (population[rand0] - population[rand1])\n\n    A trial vector is then constructed. Starting with a randomly chosen 'i'th\n    parameter the trial is sequentially filled (in modulo) with parameters from\n    ``b'`` or the original candidate. The choice of whether to use ``b'`` or the\n    original candidate is made with a binomial distribution (the 'bin' in\n    'best1bin') - a random number in [0, 1) is generated.  If this number is\n    less than the `recombination` constant then the parameter is loaded from\n    ``b'``, otherwise it is loaded from the original candidate.  The final\n    parameter is always loaded from ``b'``.  Once the trial candidate is built\n    its fitness is assessed. If the trial is better than the original candidate\n    then it takes its place. If it is also better than the best overall\n    candidate it also replaces that.\n    To improve your chances of finding a global minimum use higher `popsize`\n    values, with higher `mutation` and (dithering), but lower `recombination`\n    values. This has the effect of widening the search radius, but slowing\n    convergence.\n    By default the best solution vector is updated continuously within a single\n    iteration (``updating='immediate'``). This is a modification [4]_ of the\n    original differential evolution algorithm which can lead to faster\n    convergence as trial vectors can immediately benefit from improved\n    solutions. To use the original Storn and Price behaviour, updating the best\n    solution once per iteration, set ``updating='deferred'``.\n\n    .. versionadded:: 0.15.0\n\n    Examples\n    --------\n    Let us consider the problem of minimizing the Rosenbrock function. This\n    function is implemented in `rosen` in `scipy.optimize`.\n\n    >>> from scipy.optimize import rosen, differential_evolution\n    >>> bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]\n    >>> result = differential_evolution(rosen, bounds)\n    >>> result.x, result.fun\n    (array([1., 1., 1., 1., 1.]), 1.9216496320061384e-19)\n\n    Now repeat, but with parallelization.\n\n    >>> bounds = [(0,2), (0, 2), (0, 2), (0, 2), (0, 2)]\n    >>> result = differential_evolution(rosen, bounds, updating='deferred',\n    ...                                 workers=2)\n    >>> result.x, result.fun\n    (array([1., 1., 1., 1., 1.]), 1.9216496320061384e-19)\n\n    Let's try and do a constrained minimization\n    >>> from scipy.optimize import NonlinearConstraint, Bounds\n    >>> def constr_f(x):\n    ...     return np.array(x[0] + x[1])\n    >>>\n    >>> # the sum of x[0] and x[1] must be less than 1.9\n    >>> nlc = NonlinearConstraint(constr_f, -np.inf, 1.9)\n    >>> # specify limits using a `Bounds` object.\n    >>> bounds = Bounds([0., 0.], [2., 2.])\n    >>> result = differential_evolution(rosen, bounds, constraints=(nlc),\n    ...                                 seed=1)\n    >>> result.x, result.fun\n    (array([0.96633867, 0.93363577]), 0.0011361355854792312)\n\n    Next find the minimum of the Ackley function\n    (https://en.wikipedia.org/wiki/Test_functions_for_optimization).\n\n    >>> from scipy.optimize import differential_evolution\n    >>> import numpy as np\n    >>> def ackley(x):\n    ...     arg1 = -0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2))\n    ...     arg2 = 0.5 * (np.cos(2. * np.pi * x[0]) + np.cos(2. * np.pi * x[1]))\n    ...     return -20. * np.exp(arg1) - np.exp(arg2) + 20. + np.e\n    >>> bounds = [(-5, 5), (-5, 5)]\n    >>> result = differential_evolution(ackley, bounds)\n    >>> result.x, result.fun\n    (array([ 0.,  0.]), 4.4408920985006262e-16)\n\n    References\n    ----------\n    .. [1] Storn, R and Price, K, Differential Evolution - a Simple and\n           Efficient Heuristic for Global Optimization over Continuous Spaces,\n           Journal of Global Optimization, 1997, 11, 341 - 359.\n    .. [2] http://www1.icsi.berkeley.edu/~storn/code.html\n    .. [3] http://en.wikipedia.org/wiki/Differential_evolution\n    .. [4] Wormington, M., Panaccione, C., Matney, K. M., Bowen, D. K., -\n           Characterization of structures from X-ray scattering data using\n           genetic algorithms, Phil. Trans. R. Soc. Lond. A, 1999, 357,\n           2827-2848\n    .. [5] Lampinen, J., A constraint handling approach for the differential\n           evolution algorithm. Proceedings of the 2002 Congress on\n           Evolutionary Computation. CEC'02 (Cat. No. 02TH8600). Vol. 2. IEEE,\n           2002.\n    "
    with DifferentialEvolutionSolver(func, bounds, args=args, strategy=strategy, maxiter=maxiter, popsize=popsize, tol=tol, mutation=mutation, recombination=recombination, seed=seed, polish=polish, callback=callback, disp=disp, init=init, atol=atol, updating=updating, workers=workers, constraints=constraints) as solver:
        ret = solver.solve()
    return ret
