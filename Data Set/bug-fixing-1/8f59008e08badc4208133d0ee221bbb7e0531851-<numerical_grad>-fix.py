

def numerical_grad(f, inputs, grad_outputs, eps=0.001, detect_nondifferentiable=False, diff_atol=0, diff_rtol=0.01, center_outputs=None):
    'Computes numerical gradient by finite differences.\n\n    This function is used to implement gradient check. For usage example, see\n    unit tests of :mod:`chainer.functions`.\n\n    By default, ``numerical_grad`` computes the gradient to the first order of\n    ``eps``.\n\n    Args:\n        f (function): Python function with no arguments that runs forward\n            computation and returns the result.\n        inputs (tuple of arrays): Tuple of arrays that should be treated as\n            inputs. Each element of them is slightly modified to realize\n            numerical gradient by finite differences.\n        grad_outputs (tuple of arrays): Tuple of arrays that are treated as\n            output gradients.\n        eps (float): Epsilon value of finite differences.\n        detect_nondifferentiable (bool):\n            ``False`` by default.\n            If ``True``, ``numerical_grad`` checks whether ``f`` is\n            differentiable at ``inputs``.\n            It requires evaluation of ``f`` at 5 points instead of 2.\n            As a side effect, the accuracy of numerical gradient will be\n            increased to the third order of ``eps``.\n            If it turns out that ``f`` is non-differentiable at ``input``,\n            ``numerical_grad`` raises\n            :class:`~chainer.gradient_check.NondifferentiableError`.\n        diff_atol (float):\n            Absolute tolerance of fitting error of non-differentiable point\n            detection.\n        diff_rtol (float):\n            Tolerance of fitting error of non-differentiable point detection\n            relative to the output values of ``f``.\n        center_outputs (tuple of arrays or None):\n            Only used if ``detect_nondifferentiable`` is ``True``.\n            If specified, these arrays are used as the outputs of ``f`` at\n            ``inputs``.\n            Otherwise, it is calculated.\n            It can be used to reduce the computation if these arrays are\n            already calculated before calling ``numerical_grad``.\n\n    Returns:\n        tuple: Numerical gradient arrays corresponding to ``inputs``.\n\n    '
    assert (eps > 0)
    for x in inputs:
        if (x.dtype.kind != 'f'):
            raise RuntimeError('The dtype of input arrays must be kind of float')
    inputs = tuple(inputs)
    grad_outputs = tuple(grad_outputs)
    gpu = any((isinstance(x, cuda.ndarray) for x in (inputs + grad_outputs)))
    cpu = any((isinstance(x, numpy.ndarray) for x in (inputs + grad_outputs)))
    if (gpu and cpu):
        raise RuntimeError('Do not mix GPU and CPU arrays in `numerical_grad`')
    if gpu:
        xp = cuda.cupy
        numerical_grad_kernel_1 = cuda.reduce('T y1, T y2, U gy, T eps', 'V gxi', '(y1 - y2) * gy', 'a + b', 'gxi += a / (eps * 2)', '0', 'numerical_grad_kernel_1')
        numerical_grad_kernel_3 = cuda.reduce('T y1, T y2, T y3, T y4, U gy, T eps', 'V gxi', '(-y1 + 8 * y2 - 8 * y3 + y4) * gy', 'a + b', 'gxi += a / (eps * 6)', '0', 'numerical_grad_kernel_3')
    else:
        xp = numpy
    grads = [xp.zeros(x.shape, numpy.float64) for x in inputs]
    if detect_nondifferentiable:
        if (center_outputs is None):
            ys0 = _copy_arrays(f())
        else:
            ys0 = center_outputs
        nout = len(ys0)
        shapes = [_.shape for _ in ys0]
        sizes = numpy.array([_.size for _ in ys0])
        cumsizes = numpy.cumsum(sizes)

    def eval_func(x, i, delta, orig):
        x[i] = (orig + delta)
        y = _copy_arrays(f())
        x[i] = orig
        return y

    def iterate_single_input(i_in, x, orig_x, i):
        orig = orig_x[i]
        if detect_nondifferentiable:
            yss = [eval_func(x, i, ((- eps) * 1.0), orig), eval_func(x, i, ((- eps) * 0.5), orig), ys0, eval_func(x, i, ((+ eps) * 0.5), orig), eval_func(x, i, ((+ eps) * 1.0), orig)]
        else:
            yss = [eval_func(x, i, ((- eps) * 1), orig), eval_func(x, i, ((+ eps) * 1), orig)]
        if detect_nondifferentiable:
            any_nonfinite = False
            for i_out in range(nout):
                isfinites = [xp.isfinite(ys[i_out]) for ys in yss]
                if any(((isfinites[0] != isfinites[i]).any() for i in range(1, len(yss)))):
                    s = six.StringIO()
                    s.write('Tried to compute the numeric gradient on a non-differentiable point.\n\n')
                    s.write('i_in: {}\n'.format(i_in))
                    s.write('i_out: {}\n'.format(i_out))
                    s.write('x: {}\n'.format(inputs[i_in]))
                    s.write('index on x: {}\n'.format(i))
                    s.write('eps: {}\n'.format(eps))
                    s.write('y[x-eps  ]: {}\n'.format(yss[0][i_out]))
                    s.write('y[x-eps/2]: {}\n'.format(yss[1][i_out]))
                    s.write('y[x      ]: {}\n'.format(yss[2][i_out]))
                    s.write('y[x+eps/2]: {}\n'.format(yss[3][i_out]))
                    s.write('y[x+eps  ]: {}\n'.format(yss[4][i_out]))
                    raise NondifferentiableError(s.getvalue())
                any_nonfinite |= (not all((_.all() for _ in isfinites)))
            if (not any_nonfinite):
                ystack = xp.vstack([xp.hstack([y.ravel() for y in ys]) for ys in yss])
                assert ((ystack.ndim == 2) and (ystack.shape[0] == len(yss)))
                if gpu:
                    ystack = ystack.get()
                polyfit = numpy.polynomial.polynomial.polyfit
                (_, (residuals, _, _, _)) = polyfit(range(len(yss)), ystack, deg=2, full=True)
                if gpu:
                    residuals = xp.array(residuals)
                residuals = xp.sqrt((residuals / len(yss)))
                for i_out in range(nout):
                    size = sizes[i_out]
                    cumsize = cumsizes[i_out]
                    shape = shapes[i_out]
                    ymax = xp.concatenate([ys[i_out][None] for ys in yss]).max(axis=0)
                    ymin = xp.concatenate([ys[i_out][None] for ys in yss]).min(axis=0)
                    res = residuals[(cumsize - size):cumsize]
                    res = res.reshape(shape)
                    det = xp.asarray(((diff_atol + (diff_rtol * (ymax - ymin))) < res))
                    det[(ymax == ymin)] = False
                    if det.any():
                        s = six.StringIO()
                        s.write('Tried to compute the numeric gradient on a non-differentiable point.\n\n')
                        s.write('i_in: {}\n'.format(i_in))
                        s.write('i_out: {}\n'.format(i_out))
                        s.write('x: {}\n'.format(inputs[i_in]))
                        s.write('index on x: {}\n'.format(i))
                        s.write('eps: {}\n'.format(eps))
                        s.write('diff_rtol: {}\n'.format(diff_rtol))
                        s.write('diff_atol: {}\n'.format(diff_atol))
                        s.write('ymax: {}\n'.format(ymax))
                        s.write('ymin: {}\n'.format(ymin))
                        s.write('diff_atol + diff_rtol * (ymax-ymin): {}\n'.format((diff_atol + (diff_rtol * (ymax - ymin)))))
                        s.write('fitting errors: {}\n'.format(res))
                        s.write('y[x-eps  ]: {}\n'.format(yss[0][i_out]))
                        s.write('y[x-eps/2]: {}\n'.format(yss[1][i_out]))
                        s.write('y[x      ]: {}\n'.format(yss[2][i_out]))
                        s.write('y[x+eps/2]: {}\n'.format(yss[3][i_out]))
                        s.write('y[x+eps  ]: {}\n'.format(yss[4][i_out]))
                        raise NondifferentiableError(s.getvalue())
        for (i_out, gy) in enumerate(grad_outputs):
            if (gy is None):
                continue
            gpu_ = (gpu and all((isinstance(ys[i_out], cuda.ndarray) for ys in yss)))
            if (len(yss) == 2):
                y0 = yss[0][i_out]
                y1 = yss[1][i_out]
                if gpu_:
                    numerical_grad_kernel_1(y1, y0, xp.asarray(gy), eps, gx[i])
                else:
                    dot = ((y1 - y0) * gy).sum()
                    gx[i] += (dot / (2 * eps))
            elif (len(yss) == 5):
                y0 = yss[0][i_out]
                y1 = yss[1][i_out]
                y2 = yss[3][i_out]
                y3 = yss[4][i_out]
                if gpu_:
                    numerical_grad_kernel_3(y3, y2, y1, y0, gy, eps, gx[i])
                else:
                    num = ((((- y3) + (8 * y2)) - (8 * y1)) + y0)
                    dot = (num * gy).sum()
                    gx[i] += (dot / (6 * eps))
            else:
                assert False
    with configuration.using_config('type_check', False):
        for (i_in, (x, gx)) in enumerate(six.moves.zip(inputs, grads)):
            orig_x = x.copy()
            for i in numpy.ndindex(x.shape):
                iterate_single_input(i_in, x, orig_x, i)
    return [g.astype(x.dtype, copy=False) for (g, x) in six.moves.zip(grads, inputs)]
