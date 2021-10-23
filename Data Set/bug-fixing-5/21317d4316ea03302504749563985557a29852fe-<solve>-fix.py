def solve(self):
    '\n        Runs the DifferentialEvolutionSolver.\n\n        Returns\n        -------\n        res : OptimizeResult\n            The optimization result represented as a ``OptimizeResult`` object.\n            Important attributes are: ``x`` the solution array, ``success`` a\n            Boolean flag indicating if the optimizer exited successfully and\n            ``message`` which describes the cause of the termination. See\n            `OptimizeResult` for a description of other attributes.  If `polish`\n            was employed, and a lower minimum was obtained by the polishing,\n            then OptimizeResult also contains the ``jac`` attribute.\n        '
    (nit, warning_flag) = (0, False)
    status_message = _status_message['success']
    if np.all(np.isinf(self.population_energies)):
        self._calculate_population_energies()
    for nit in xrange(1, (self.maxiter + 1)):
        try:
            next(self)
        except StopIteration:
            warning_flag = True
            status_message = _status_message['maxfev']
            break
        if self.disp:
            print(('differential_evolution step %d: f(x)= %g' % (nit, self.population_energies[0])))
        convergence = self.convergence
        if (self.callback and (self.callback(self._scale_parameters(self.population[0]), convergence=(self.tol / convergence)) is True)):
            warning_flag = True
            status_message = 'callback function requested stop early by returning True'
            break
        intol = (np.std(self.population_energies) <= (self.atol + (self.tol * np.abs(np.mean(self.population_energies)))))
        if (warning_flag or intol):
            break
    else:
        status_message = _status_message['maxiter']
        warning_flag = True
    DE_result = OptimizeResult(x=self.x, fun=self.population_energies[0], nfev=self._nfev, nit=nit, message=status_message, success=(warning_flag is not True))
    if self.polish:
        result = minimize(self.func, np.copy(DE_result.x), method='L-BFGS-B', bounds=self.limits.T, args=self.args)
        self._nfev += result.nfev
        DE_result.nfev = self._nfev
        if (result.fun < DE_result.fun):
            DE_result.fun = result.fun
            DE_result.x = result.x
            DE_result.jac = result.jac
            self.population_energies[0] = result.fun
            self.population[0] = self._unscale_parameters(result.x)
    return DE_result