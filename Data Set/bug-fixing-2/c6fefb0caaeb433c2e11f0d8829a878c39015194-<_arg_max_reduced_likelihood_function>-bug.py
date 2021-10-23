

def _arg_max_reduced_likelihood_function(self):
    '\n        This function estimates the autocorrelation parameters theta as the\n        maximizer of the reduced likelihood function.\n        (Minimization of the opposite reduced likelihood function is used for\n        convenience)\n\n        Parameters\n        ----------\n        self : All parameters are stored in the Gaussian Process model object.\n\n        Returns\n        -------\n        optimal_theta : array_like\n            The best set of autocorrelation parameters (the sought maximizer of\n            the reduced likelihood function).\n\n        optimal_reduced_likelihood_function_value : double\n            The optimal reduced likelihood function value.\n\n        optimal_par : dict\n            The BLUP parameters associated to thetaOpt.\n        '
    best_optimal_theta = []
    best_optimal_rlf_value = []
    best_optimal_par = []
    if self.verbose:
        print(('The chosen optimizer is: ' + str(self.optimizer)))
        if (self.random_start > 1):
            print((str(self.random_start) + ' random starts are required.'))
    percent_completed = 0.0
    if ((self.optimizer == 'Welch') and (self.theta0.size == 1)):
        self.optimizer = 'fmin_cobyla'
    if (self.optimizer == 'fmin_cobyla'):

        def minus_reduced_likelihood_function(log10t):
            return (- self.reduced_likelihood_function(theta=(10.0 ** log10t))[0])
        constraints = []
        for i in range(self.theta0.size):
            constraints.append((lambda log10t, i=i: (log10t[i] - np.log10(self.thetaL[(0, i)]))))
            constraints.append((lambda log10t, i=i: (np.log10(self.thetaU[(0, i)]) - log10t[i])))
        for k in range(self.random_start):
            if (k == 0):
                theta0 = self.theta0
            else:
                log10theta0 = (np.log10(self.thetaL) + (self.random_state.rand(*self.theta0.shape) * np.log10((self.thetaU / self.thetaL))))
                theta0 = (10.0 ** log10theta0)
            try:
                log10_optimal_theta = optimize.fmin_cobyla(minus_reduced_likelihood_function, np.log10(theta0).ravel(), constraints, iprint=0)
            except ValueError as ve:
                print('Optimization failed. Try increasing the ``nugget``')
                raise ve
            optimal_theta = (10.0 ** log10_optimal_theta)
            (optimal_rlf_value, optimal_par) = self.reduced_likelihood_function(theta=optimal_theta)
            if (k > 0):
                if (optimal_rlf_value > best_optimal_rlf_value):
                    best_optimal_rlf_value = optimal_rlf_value
                    best_optimal_par = optimal_par
                    best_optimal_theta = optimal_theta
            else:
                best_optimal_rlf_value = optimal_rlf_value
                best_optimal_par = optimal_par
                best_optimal_theta = optimal_theta
            if (self.verbose and (self.random_start > 1)):
                if (((20 * k) / self.random_start) > percent_completed):
                    percent_completed = ((20 * k) / self.random_start)
                    print(('%s completed' % (5 * percent_completed)))
        optimal_rlf_value = best_optimal_rlf_value
        optimal_par = best_optimal_par
        optimal_theta = best_optimal_theta
    elif (self.optimizer == 'Welch'):
        (theta0, thetaL, thetaU) = (self.theta0, self.thetaL, self.thetaU)
        corr = self.corr
        verbose = self.verbose
        self.optimizer = 'fmin_cobyla'
        self.verbose = False
        if verbose:
            print('Initialize under isotropy assumption...')
        self.theta0 = check_array(self.theta0.min())
        self.thetaL = check_array(self.thetaL.min())
        self.thetaU = check_array(self.thetaU.max())
        (theta_iso, optimal_rlf_value_iso, par_iso) = self._arg_max_reduced_likelihood_function()
        optimal_theta = (theta_iso + np.zeros(theta0.shape))
        if verbose:
            print('Now improving allowing for anisotropy...')
        for i in self.random_state.permutation(theta0.size):
            if verbose:
                print(('Proceeding along dimension %d...' % (i + 1)))
            self.theta0 = check_array(theta_iso)
            self.thetaL = check_array(thetaL[(0, i)])
            self.thetaU = check_array(thetaU[(0, i)])

            def corr_cut(t, d):
                return corr(check_array(np.hstack([optimal_theta[0][0:i], t[0], optimal_theta[0][(i + 1):]])), d)
            self.corr = corr_cut
            (optimal_theta[(0, i)], optimal_rlf_value, optimal_par) = self._arg_max_reduced_likelihood_function()
        (self.theta0, self.thetaL, self.thetaU) = (theta0, thetaL, thetaU)
        self.corr = corr
        self.optimizer = 'Welch'
        self.verbose = verbose
    else:
        raise NotImplementedError(("This optimizer ('%s') is not implemented yet. Please contribute!" % self.optimizer))
    return (optimal_theta, optimal_rlf_value, optimal_par)
