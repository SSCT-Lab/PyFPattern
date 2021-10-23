def _directional_numeric_gradients(self, directions, y0_data):
    device = self.device
    func = self.func
    x_data = self.x_data
    y_grad = self.y_grad
    params = self.params
    eps = self.eps
    no_grads = self.no_grads
    dtype = self.dtype
    detect_nondifferentiable = self.detect_nondifferentiable
    params_data = [(p if self.is_immutable_params else p.array) for p in params]
    xp = device.xp
    x_vars = [variable.Variable(x, requires_grad=False) for x in x_data]
    x_data_filtered = [x.array for (x, skip) in six.moves.zip(x_vars, no_grads) if (not skip)]
    if (dtype is None):
        casted_data = [x for x in (x_data_filtered + params_data)]
    else:
        if (numpy.dtype(dtype).kind != 'f'):
            raise ValueError('`dtype` is allowed only float type')
        for (x, skip) in six.moves.zip(x_vars, no_grads):
            if (skip and (x.array.dtype.kind == 'f')):
                x.array = x.array.astype(dtype, copy=False)
        casted_data = [x.astype(dtype, copy=False) for x in (x_data_filtered + params_data)]
    delta = xp.array(0.0, numpy.float64)

    def g():

        def perturb(data, direction):
            data = (data.astype(numpy.float64) + (delta * direction)).astype(data.dtype)
            if numpy.isscalar(data):
                data = xp.array(data)
            return data
        g_x_vars = []
        j = 0
        for (x_var, skip) in six.moves.zip(x_vars, no_grads):
            if skip:
                g_x_vars.append(x_var)
            else:
                data = perturb(casted_data[j], directions[j])
                g_x_vars.append(variable.Variable(data))
                j += 1
        for i in range(len(params)):
            data = perturb(casted_data[(j + i)], directions[(j + i)])
            if self.is_immutable_params:
                params_data[i] = data
            else:
                params[i].array = data
        self._clear_grads(g_x_vars)
        if (not self.is_immutable_params):
            self._clear_grads(params)
        if self.is_immutable_params:
            ps = tuple([chainer.Parameter(p) for p in params_data])
            ys = func(g_x_vars, ps)
        else:
            ys = func(*g_x_vars)
        ys = _as_tuple(ys)
        ys_data = tuple([(None if (y is None) else y.array) for y in ys])
        if (xp is chainerx):
            ys_data = tuple([(None if (y is None) else y.as_grad_stopped()) for y in ys_data])
        if (not self.is_immutable_params):
            for (i, param) in enumerate(params):
                param.array = casted_data[(j + i)]
        return ys_data
    (gx,) = numerical_grad(g, (delta,), y_grad, eps=eps, detect_nondifferentiable=detect_nondifferentiable, center_outputs=y0_data, diff_atol=0, diff_rtol=self.rtol)
    return gx