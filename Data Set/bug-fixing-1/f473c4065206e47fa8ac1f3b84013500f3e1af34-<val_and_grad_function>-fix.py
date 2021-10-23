

def val_and_grad_function(f, params=None):
    'Returns a function that computes f and its derivative w.r.t. params.\n\n  Example:\n  ```python\n  # f(x, y) = (x ^ 3) * y - x * (y ^ 2)\n  # Therefore, the 1st order derivatives are:\n  #   df / dx = 3 * (x ^ 2) * y - y ^ 2\n  #   df / dy = x ^ 3 - 2 * x * y\n  def f(x, y):\n    return x * x * x * y - x * y * y\n\n  # Obtain a function that returns the function value and the 1st order\n  # gradients.\n  val_grads_fn = tfe.value_and_gradients_function(f)\n\n  x = 2.0\n  y = 3.0\n\n  # Invoke the value-and-gradients function.\n  f_val, (x_grad, y_grad) = val_grads_fn(x, y)\n  assert f_val.numpy() == (2 ** 3) * 3 - 2 * (3 ** 2)\n  assert x_grad.numpy() == 3 * (2 ** 2) * 3 - 3 ** 2\n  assert y_grad.numpy() == (2 ** 3) - 2 * 2 * 3\n\n  # To obtain a callable that returns the value of `f` and the gradient(s) of\n  # `f` with respect to a subset of its inputs, use the `params` keyword\n  # argument with `value_and_gradients_function()`.\n  val_ygrad_fn = tfe.value_and_gradients_function(f, params=[1])\n\n  f_val, (y_grad,) = val_ygrad_fn(x, y)\n  assert f_val.numpy() == (2 ** 3) * 3 - 2 * (3 ** 2)\n  assert y_grad.numpy() == (2 ** 3) - 2 * 2 * 3\n  ```\n\n  Args:\n   f: function to be differentiated. If `f` returns a scalar, this scalar will\n     be differentiated. If `f` returns a tensor or list of tensors, by default\n     a scalar will be computed by adding all their values to produce a single\n     scalar. If desired, the tensors can be elementwise multiplied by the\n     tensors passed as the `dy` keyword argument to the returned gradient\n     function.\n   params: list of parameter names of f or list of integers indexing the\n     parameters with respect to which we\'ll differentiate. Passing `None`\n     differentiates with respect to all parameters.\n\n  Returns: function which, when called, returns the value of f and the gradient\n   of f with respect to all of `params`. The function takes an extra optional\n   keyword argument "dy". Setting it allows computation of vector jacobian\n   products for vectors other than the vector of ones.\n\n  Raises:\n   ValueError: if the params are not all strings or all integers.\n  '

    def decorated(*args, **kwds):
        'Computes the value and gradient of the decorated function.'
        dy = kwds.pop('dy', None)
        if kwds:
            raise ValueError('Functions to be differentiated cannot receive keyword arguments.')
        (val, vjp) = make_vjp(f, params)(*args, **kwds)
        return (val, vjp(dy=dy))
    return decorated
