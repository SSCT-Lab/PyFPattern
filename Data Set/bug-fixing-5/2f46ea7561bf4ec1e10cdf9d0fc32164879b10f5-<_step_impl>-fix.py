def _step_impl(self):
    t = self.t
    D = self.D
    max_step = self.max_step
    min_step = (10 * np.abs((np.nextafter(t, (self.direction * np.inf)) - t)))
    if (self.h_abs > max_step):
        h_abs = max_step
        change_D(D, self.order, (max_step / self.h_abs))
        self.n_equal_steps = 0
    elif (self.h_abs < min_step):
        h_abs = min_step
        change_D(D, self.order, (min_step / self.h_abs))
        self.n_equal_steps = 0
    else:
        h_abs = self.h_abs
    atol = self.atol
    rtol = self.rtol
    order = self.order
    alpha = self.alpha
    gamma = self.gamma
    error_const = self.error_const
    J = self.J
    LU = self.LU
    current_jac = (self.jac is None)
    step_accepted = False
    while (not step_accepted):
        if (h_abs < min_step):
            return (False, self.TOO_SMALL_STEP)
        h = (h_abs * self.direction)
        t_new = (t + h)
        if ((self.direction * (t_new - self.t_bound)) > 0):
            t_new = self.t_bound
            change_D(D, order, (np.abs((t_new - t)) / h_abs))
            self.n_equal_steps = 0
            LU = None
        h = (t_new - t)
        h_abs = np.abs(h)
        y_predict = np.sum(D[:(order + 1)], axis=0)
        scale = (atol + (rtol * np.abs(y_predict)))
        psi = (np.dot(D[1:(order + 1)].T, gamma[1:(order + 1)]) / alpha[order])
        converged = False
        c = (h / alpha[order])
        while (not converged):
            if (LU is None):
                LU = self.lu((self.I - (c * J)))
            (converged, n_iter, y_new, d) = solve_bdf_system(self.fun, t_new, y_predict, c, psi, LU, self.solve_lu, scale, self.newton_tol)
            if (not converged):
                if current_jac:
                    break
                J = self.jac(t_new, y_predict)
                LU = None
                current_jac = True
        if (not converged):
            factor = 0.5
            h_abs *= factor
            change_D(D, order, factor)
            self.n_equal_steps = 0
            LU = None
            continue
        safety = ((0.9 * ((2 * NEWTON_MAXITER) + 1)) / ((2 * NEWTON_MAXITER) + n_iter))
        scale = (atol + (rtol * np.abs(y_new)))
        error = (error_const[order] * d)
        error_norm = norm((error / scale))
        if (error_norm > 1):
            factor = max(MIN_FACTOR, (safety * (error_norm ** ((- 1) / (order + 1)))))
            h_abs *= factor
            change_D(D, order, factor)
            self.n_equal_steps = 0
        else:
            step_accepted = True
    self.n_equal_steps += 1
    self.t = t_new
    self.y = y_new
    self.h_abs = h_abs
    self.J = J
    self.LU = LU
    D[(order + 2)] = (d - D[(order + 1)])
    D[(order + 1)] = d
    for i in reversed(range((order + 1))):
        D[i] += D[(i + 1)]
    if (self.n_equal_steps < (order + 1)):
        return (True, None)
    if (order > 1):
        error_m = (error_const[(order - 1)] * D[order])
        error_m_norm = norm((error_m / scale))
    else:
        error_m_norm = np.inf
    if (order < MAX_ORDER):
        error_p = (error_const[(order + 1)] * D[(order + 2)])
        error_p_norm = norm((error_p / scale))
    else:
        error_p_norm = np.inf
    error_norms = np.array([error_m_norm, error_norm, error_p_norm])
    with np.errstate(divide='ignore'):
        factors = (error_norms ** ((- 1) / np.arange(order, (order + 3))))
    delta_order = (np.argmax(factors) - 1)
    order += delta_order
    self.order = order
    factor = min(MAX_FACTOR, (safety * np.max(factors)))
    self.h_abs *= factor
    change_D(D, order, factor)
    self.n_equal_steps = 0
    self.LU = None
    return (True, None)