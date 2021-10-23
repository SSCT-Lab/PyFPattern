def numeric_grad(executor, location, aux_states=None, eps=0.0001, use_forward_train=True):
    "Calculates a numeric gradient via finite difference method.\n\n    Class based on Theano's `theano.gradient.numeric_grad` [1]\n\n    Parameters\n    ----------\n    executor : Executor\n        exectutor that computes the forward pass\n    location : list of numpy.ndarray or dict of str to numpy.ndarray\n        Argument values used as location to compute gradient\n        Maps the name of arguments to the corresponding numpy.ndarray.\n        Value of all the arguments must be provided.\n    aux_states : None or list of numpy.ndarray or dict of str to numpy.ndarray, optional\n        Auxiliary states values used as location to compute gradient\n        Maps the name of aux_states to the corresponding numpy.ndarray.\n        Value of all the auxiliary arguments must be provided.\n    eps : float, optional\n        epsilon for the finite-difference method\n    use_forward_train : bool, optional\n        Whether to use `is_train=True` in testing.\n    References\n    ---------\n    ..[1] https://github.com/Theano/Theano/blob/master/theano/gradient.py\n    "
    for (k, v) in location.items():
        executor.arg_dict[k][:] = v
    approx_grads = {k: np.zeros(v.shape, dtype=np.float32) for (k, v) in location.items()}
    executor.forward(is_train=use_forward_train)
    f_x = executor.outputs[0].asnumpy()[0]
    for k in location:
        location[k] = np.ascontiguousarray(location[k])
    for (k, v) in location.items():
        old_value = v.copy()
        for i in range(np.prod(v.shape)):
            v.ravel()[i] += eps
            executor.arg_dict[k][:] = v
            if (aux_states is not None):
                for (key, val) in aux_states.items():
                    executor.aux_dict[key][:] = val
            executor.forward(is_train=use_forward_train)
            f_eps = executor.outputs[0].asnumpy()[0]
            approx_grads[k].ravel()[i] = ((f_eps - f_x) / eps)
            v.ravel()[i] = old_value.ravel()[i]
        executor.arg_dict[k][:] = old_value
    return approx_grads