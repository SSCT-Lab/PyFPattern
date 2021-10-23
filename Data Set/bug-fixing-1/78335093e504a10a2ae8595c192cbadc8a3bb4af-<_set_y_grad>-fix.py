

def _set_y_grad(y, y_grad):
    if (y_grad is not None):
        if (len(y) != len(y_grad)):
            raise ValueError('Upstream gradients must contain equally many elements as number of output elements.\nActual: {} != {}'.format(len(y), len(y_grad)))
        for (iy, igy) in six.moves.zip(y, y_grad):
            if isinstance(igy, variable.Variable):
                iy.grad_var = igy
            else:
                iy.grad = igy
    else:
        if (len(y) != 1):
            raise ValueError('Function must return a zero-dimensional array of length 1 if the upstream gradient is `None`.\nActual: {} != 1'.format(len(y)))
        y_grad = (1,)
    return y_grad
