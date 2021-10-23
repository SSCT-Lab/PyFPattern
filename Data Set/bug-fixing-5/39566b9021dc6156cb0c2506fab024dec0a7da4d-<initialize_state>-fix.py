def initialize_state(self, variance=None, complex_step=False):
    '\n        Initialize state and state covariance arrays in preparation for the\n        Kalman filter.\n\n        Parameters\n        ----------\n        variance : float, optional\n            The variance for approximating diffuse initial conditions. Default\n            can be found in the Representation class documentation.\n\n        Notes\n        -----\n        Initializes the ARMA component of the state space to the typical\n        stationary values and the other components as approximate diffuse.\n\n        Can be overridden be calling one of the other initialization methods\n        before fitting the model.\n        '
    if self._manual_initialization:
        return
    if (not self.enforce_stationarity):
        self.initialize_approximate_diffuse(variance)
        return
    if (variance is None):
        variance = self.ssm.initial_variance
    dtype = self.ssm.transition.dtype
    initial_state = np.zeros(self.k_states, dtype=dtype)
    initial_state_cov = (np.eye(self.k_states, dtype=dtype) * variance)
    if self.state_regression:
        start = (- (self.k_exog + self._k_order))
        end = ((- self.k_exog) if (self.k_exog > 0) else None)
    else:
        start = (- self._k_order)
        end = None
    if (self._k_order > 0):
        transition = self.ssm['transition', start:end, start:end, 0]
        if ((not self.hamilton_representation) and (self.k_trend > 0)):
            initial_intercept = self[('state_intercept', self._k_states_diff, 0)]
            initial_mean = (initial_intercept / (1 - np.sum(transition[:, 0])))
            initial_state[self._k_states_diff] = initial_mean
            _start = (self._k_states_diff + 1)
            _end = ((_start + transition.shape[0]) - 1)
            initial_state[_start:_end] = (transition[1:, 0] * initial_mean)
        selection_stationary = self.ssm['selection', start:end, :, 0]
        selected_state_cov_stationary = np.dot(np.dot(selection_stationary, self.ssm['state_cov', :, :, 0]), selection_stationary.T)
        initial_state_cov_stationary = solve_discrete_lyapunov(transition, selected_state_cov_stationary, complex_step=complex_step)
        initial_state_cov[start:end, start:end] = initial_state_cov_stationary
    self.ssm.initialize_known(initial_state, initial_state_cov)