def _set_y_grad(y, y_grad):
    if (y_grad is not None):
        if (len(y) != len(y_grad)):
            raise ValueError('`y_grad` must have the same length of output values')
        for (iy, igy) in six.moves.zip(y, y_grad):
            if isinstance(igy, variable.Variable):
                iy.grad_var = igy
            else:
                iy.grad = igy
    else:
        if (len(y) != 1):
            raise ValueError('When `y_grad` is `None`, the function must return azero-dimentional array')
        y_grad = (1,)
    return y_grad