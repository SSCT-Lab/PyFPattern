def __init__(self, func, bounds, args=(), strategy='best1bin', maxiter=1000, popsize=15, tol=0.01, mutation=(0.5, 1), recombination=0.7, seed=None, maxfun=np.inf, callback=None, disp=False, polish=True, init='latinhypercube'):
    if (strategy in self._binomial):
        self.mutation_func = getattr(self, self._binomial[strategy])
    elif (strategy in self._exponential):
        self.mutation_func = getattr(self, self._exponential[strategy])
    else:
        raise ValueError('Please select a valid mutation strategy')
    self.strategy = strategy
    self.callback = callback
    self.polish = polish
    self.tol = tol
    self.scale = mutation
    if ((not np.all(np.isfinite(mutation))) or np.any((np.array(mutation) >= 2)) or np.any((np.array(mutation) < 0))):
        raise ValueError('The mutation constant must be a float in U[0, 2), or specified as a tuple(min, max) where min < max and min, max are in U[0, 2).')
    self.dither = None
    if (hasattr(mutation, '__iter__') and (len(mutation) > 1)):
        self.dither = [mutation[0], mutation[1]]
        self.dither.sort()
    self.cross_over_probability = recombination
    self.func = func
    self.args = args
    self.limits = np.array(bounds, dtype='float').T
    if ((np.size(self.limits, 0) != 2) or (not np.all(np.isfinite(self.limits)))):
        raise ValueError('bounds should be a sequence containing real valued (min, max) pairs for each value in x')
    if (maxiter is None):
        maxiter = 1000
    self.maxiter = maxiter
    if (maxfun is None):
        maxfun = np.inf
    self.maxfun = maxfun
    self.__scale_arg1 = (0.5 * (self.limits[0] + self.limits[1]))
    self.__scale_arg2 = np.fabs((self.limits[0] - self.limits[1]))
    self.parameter_count = np.size(self.limits, 1)
    self.random_number_generator = check_random_state(seed)
    self.num_population_members = (popsize * self.parameter_count)
    self.population_shape = (self.num_population_members, self.parameter_count)
    self._nfev = 0
    if (init == 'latinhypercube'):
        self.init_population_lhs()
    elif (init == 'random'):
        self.init_population_random()
    else:
        raise ValueError("The population initialization method must be oneof 'latinhypercube' or 'random'")
    self.disp = disp