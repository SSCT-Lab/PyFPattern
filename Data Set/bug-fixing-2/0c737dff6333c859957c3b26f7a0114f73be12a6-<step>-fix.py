

def step(self, closure):
    'Performs a single optimization step.\n\n        Arguments:\n            closure (callable): A closure that reevaluates the model\n                and returns the loss.\n        '
    assert (len(self.param_groups) == 1)
    group = self.param_groups[0]
    lr = group['lr']
    max_iter = group['max_iter']
    max_eval = group['max_eval']
    tolerance_grad = group['tolerance_grad']
    tolerance_change = group['tolerance_change']
    line_search_fn = group['line_search_fn']
    history_size = group['history_size']
    state = self.state[self._params[0]]
    state.setdefault('func_evals', 0)
    state.setdefault('n_iter', 0)
    orig_loss = closure()
    loss = float(orig_loss)
    current_evals = 1
    state['func_evals'] += 1
    flat_grad = self._gather_flat_grad()
    abs_grad_sum = flat_grad.abs().sum()
    if (abs_grad_sum <= tolerance_grad):
        return loss
    d = state.get('d')
    t = state.get('t')
    old_dirs = state.get('old_dirs')
    old_stps = state.get('old_stps')
    H_diag = state.get('H_diag')
    prev_flat_grad = state.get('prev_flat_grad')
    prev_loss = state.get('prev_loss')
    n_iter = 0
    while (n_iter < max_iter):
        n_iter += 1
        state['n_iter'] += 1
        if (state['n_iter'] == 1):
            d = flat_grad.neg()
            old_dirs = []
            old_stps = []
            H_diag = 1
        else:
            y = flat_grad.sub(prev_flat_grad)
            s = d.mul(t)
            ys = y.dot(s)
            if (ys > 1e-10):
                if (len(old_dirs) == history_size):
                    old_dirs.pop(0)
                    old_stps.pop(0)
                old_dirs.append(y)
                old_stps.append(s)
                H_diag = (ys / y.dot(y))
            num_old = len(old_dirs)
            if ('ro' not in state):
                state['ro'] = ([None] * history_size)
                state['al'] = ([None] * history_size)
            ro = state['ro']
            al = state['al']
            for i in range(num_old):
                ro[i] = (1.0 / old_dirs[i].dot(old_stps[i]))
            q = flat_grad.neg()
            for i in range((num_old - 1), (- 1), (- 1)):
                al[i] = (old_stps[i].dot(q) * ro[i])
                q.add_((- al[i]), old_dirs[i])
            d = r = torch.mul(q, H_diag)
            for i in range(num_old):
                be_i = (old_dirs[i].dot(r) * ro[i])
                r.add_((al[i] - be_i), old_stps[i])
        if (prev_flat_grad is None):
            prev_flat_grad = flat_grad.clone()
        else:
            prev_flat_grad.copy_(flat_grad)
        prev_loss = loss
        if (state['n_iter'] == 1):
            t = (min(1.0, (1.0 / abs_grad_sum)) * lr)
        else:
            t = lr
        gtd = flat_grad.dot(d)
        ls_func_evals = 0
        if (line_search_fn is not None):
            raise RuntimeError('line search function is not supported yet')
        else:
            self._add_grad(t, d)
            if (n_iter != max_iter):
                loss = float(closure())
                flat_grad = self._gather_flat_grad()
                abs_grad_sum = flat_grad.abs().sum()
                ls_func_evals = 1
        current_evals += ls_func_evals
        state['func_evals'] += ls_func_evals
        if (n_iter == max_iter):
            break
        if (current_evals >= max_eval):
            break
        if (abs_grad_sum <= tolerance_grad):
            break
        if (gtd > (- tolerance_change)):
            break
        if (d.mul(t).abs_().sum() <= tolerance_change):
            break
        if (abs((loss - prev_loss)) < tolerance_change):
            break
    state['d'] = d
    state['t'] = t
    state['old_dirs'] = old_dirs
    state['old_stps'] = old_stps
    state['H_diag'] = H_diag
    state['prev_flat_grad'] = prev_flat_grad
    state['prev_loss'] = prev_loss
    return orig_loss
