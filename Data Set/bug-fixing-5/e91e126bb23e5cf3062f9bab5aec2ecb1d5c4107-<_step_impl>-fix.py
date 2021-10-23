def _step_impl(self):
    t = self.t
    y = self.y
    max_step = self.max_step
    rtol = self.rtol
    atol = self.atol
    min_step = (10 * np.abs((np.nextafter(t, (self.direction * np.inf)) - t)))
    if (self.h_abs > max_step):
        h_abs = max_step
    elif (self.h_abs < min_step):
        h_abs = min_step
    else:
        h_abs = self.h_abs
    order = self.order
    step_accepted = False
    while (not step_accepted):
        if (h_abs < min_step):
            return (False, self.TOO_SMALL_STEP)
        h = (h_abs * self.direction)
        t_new = (t + h)
        if ((self.direction * (t_new - self.t_bound)) > 0):
            t_new = self.t_bound
        h = (t_new - t)
        h_abs = np.abs(h)
        (y_new, f_new, error) = rk_step(self.fun, t, y, self.f, h, self.A, self.B, self.C, self.E, self.K)
        scale = (atol + (np.maximum(np.abs(y), np.abs(y_new)) * rtol))
        error_norm = norm((error / scale))
        if (error_norm == 0.0):
            h_abs *= MAX_FACTOR
            step_accepted = True
        elif (error_norm < 1):
            h_abs *= min(MAX_FACTOR, max(1, (SAFETY * (error_norm ** ((- 1) / (order + 1))))))
            step_accepted = True
        else:
            h_abs *= max(MIN_FACTOR, (SAFETY * (error_norm ** ((- 1) / (order + 1)))))
    self.y_old = y
    self.t = t_new
    self.y = y_new
    self.h_abs = h_abs
    self.f = f_new
    return (True, None)