

def rvs_ratio_uniforms(pdf, umax, vmin, vmax, size=1, c=0, random_state=None):
    '\n    Generate random samples from a probability density function using the\n    ratio-of-uniforms method.\n\n    Parameters\n    ----------\n    pdf : callable\n        A function with signature `pdf(x)` that is the probability\n        density function of the distribution.\n    umax : float\n        The upper bound of the bounding rectangle in the u-direction.\n    vmin : float\n        The lower bound of the bounding rectangle in the v-direction.\n    vmax : float\n        The upper bound of the bounding rectangle in the v-direction.\n    size : int or tuple of ints, optional\n        Defining number of random variates (default is 1).\n    c : float, optional.\n        Shift parameter of ratio-of-uniforms method, see Notes. Default is 0.\n    random_state : int or np.random.RandomState instance, optional\n        If already a RandomState instance, use it.\n        If seed is an int, return a new RandomState instance seeded with seed.\n        If None, use np.random.RandomState. Default is None.\n\n    Returns\n    -------\n    rvs : ndarray\n        The random variates distributed according to the probability\n        distribution defined by the pdf.\n\n    Notes\n    -----\n    Given a univariate probability density function `pdf` and a constant `c`,\n    define the set ``A = {(u, v) : 0 < u <= sqrt(pdf(v/u + c))}``.\n    If `(U, V)` is a random vector uniformly distributed over `A`,\n    then `V/U + c` follows a distribution according to `pdf`.\n\n    The above result (see [1]_, [2]_) can be used to sample random variables\n    using only the pdf, i.e. no inversion of the cdf is required. Typical\n    choices of `c` are zero or the mode of `pdf`. The set `A` is a subset of\n    the rectangle ``R = [0, umax] x [vmin, vmax]`` where\n\n    - ``umax = sup sqrt(pdf(x))``\n    - ``vmin = inf (x - c) sqrt(pdf(x))``\n    - ``vmax = sup (x - c) sqrt(pdf(x))``\n\n    In particular, these values are finite if `pdf` is bounded and\n    ``x**2 * pdf(x)`` is bounded (i.e. subquadratic tails).\n    One can generate `(U, V)` uniformly on `R` and return\n    `V/U + c` if `(U, V)` are also in `A` which can be directly\n    verified.\n\n    Intuitively, the method works well if `A` fills up most of the\n    enclosing rectangle such that the probability is high that `(U, V)`\n    lies in `A` whenever it lies in `R` as the number of required\n    iterations becomes too large otherwise. To be more precise, note that\n    the expected number of iterations to draw `(U, V)` uniformly\n    distributed on `R` such that `(U, V)` is also in `A` is given by\n    the ratio ``area(R) / area(A) = 2 * umax * (vmax - vmin)``, using the fact\n    that the area of `A` is equal to 1/2 (Theorem 7.1 in [1]_). A warning\n    is displayed if this ratio is larger than 20. Moreover, if the sampling\n    fails to generate a single random variate after 50000 iterations (i.e.\n    not a single draw is in `A`), an exception is raised.\n\n    If the bounding rectangle is not correctly specified (i.e. if it does not\n    contain `A`), the algorithm samples from a distribution different from\n    the one given by `pdf`. It is therefore recommended to perform a\n    test such as `~scipy.stats.kstest` as a check.\n\n    References\n    ----------\n    .. [1] L. Devroye, "Non-Uniform Random Variate Generation",\n       Springer-Verlag, 1986.\n\n    .. [2] W. Hoermann and J. Leydold, "Generating generalized inverse Gaussian\n       random variates", Statistics and Computing, 24(4), p. 547--557, 2014.\n\n    .. [3] A.J. Kinderman and J.F. Monahan, "Computer Generation of Random\n       Variables Using the Ratio of Uniform Deviates",\n       ACM Transactions on Mathematical Software, 3(3), p. 257--260, 1977.\n\n    Examples\n    --------\n    >>> from scipy import stats\n\n    Simulate normally distributed random variables. It is easy to compute the\n    bounding rectangle explicitly in that case.\n\n    >>> f = stats.norm.pdf\n    >>> v_bound = np.sqrt(f(np.sqrt(2))) * np.sqrt(2)\n    >>> umax, vmin, vmax = np.sqrt(f(0)), -v_bound, v_bound\n    >>> np.random.seed(12345)\n    >>> rvs = stats.rvs_ratio_uniforms(f, umax, vmin, vmax, size=2500)\n\n    The K-S test confirms that the random variates are indeed normally\n    distributed (normality is not rejected at 5% significance level):\n\n    >>> stats.kstest(rvs, \'norm\')[1]\n    0.3420173467307603\n\n    The exponential distribution provides another example where the bounding\n    rectangle can be determined explicitly.\n\n    >>> np.random.seed(12345)\n    >>> rvs = stats.rvs_ratio_uniforms(lambda x: np.exp(-x), umax=1,\n    ...                                vmin=0, vmax=2*np.exp(-1), size=1000)\n    >>> stats.kstest(rvs, \'expon\')[1]\n    0.928454552559516\n\n    Sometimes it can be helpful to use a non-zero shift parameter `c`, see e.g.\n    [2]_ above in the case of the generalized inverse Gaussian distribution.\n\n    '
    if (vmin >= vmax):
        raise ValueError('vmin must be smaller than vmax.')
    if (umax <= 0):
        raise ValueError('umax must be positive.')
    exp_iter = ((2 * (vmax - vmin)) * umax)
    if (exp_iter > 20):
        msg = 'The expected number of iterations to generate a single random number from the desired distribution is larger than {}, potentially causing bad performance.'.format(int(exp_iter))
        warnings.warn(msg, RuntimeWarning)
    size1d = tuple(np.atleast_1d(size))
    N = np.prod(size1d)
    rng = check_random_state(random_state)
    x = np.zeros(N)
    (simulated, i) = (0, 1)
    while True:
        k = (N - simulated)
        u1 = (umax * rng.random_sample(size=k))
        v1 = (vmin + ((vmax - vmin) * rng.random_sample(size=k)))
        rvs = ((v1 / u1) + c)
        accept = ((u1 ** 2) <= pdf(rvs))
        num_accept = np.sum(accept)
        if (num_accept > 0):
            take = min(num_accept, (N - simulated))
            x[simulated:(simulated + take)] = rvs[accept][0:take]
            simulated += take
        if (simulated >= N):
            return np.reshape(x, size1d)
        if ((simulated == 0) and ((i * N) >= 50000)):
            msg = 'Not a single random variate could be generated in {} attempts. The ratio of uniforms method does not appear to work for the provided parameters. Please check the pdf and the bounds.'.format((i * N))
            raise RuntimeError(msg)
        i += 1
