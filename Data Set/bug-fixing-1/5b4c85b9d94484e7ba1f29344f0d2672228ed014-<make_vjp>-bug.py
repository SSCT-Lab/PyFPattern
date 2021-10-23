

def make_vjp(f, params=None, persistent=True):
    'Returns a function that computes f and is vjp w.r.t. params.\n\n  The term "vjp" here is an abbreviation for vector-jacobian product.\n\n  Args:\n    f: the function to be differentiated.\n    params: the parameters (numbers or names) to differentiate with respect to.\n       A value of None will differentiate with respect to all parameters.\n    persistent: Boolean controlling whether the VJP function can be re-used.\n      Must be True or False.\n\n  Returns:\n    A function, which when called, returns a tuple (value, vjp), where:\n    - value is the result of calling f.\n    - vjp is a function, which takes a vector as an argument and\n      returns the product of that vector with the Jacobian of f.\n      Providing no argument to vjp is equivalent to providing a\n      vector of ones.\n\n    For example,\n    ```python\n    def f(x):\n      return x * x\n\n    wrapped_fn = tfe.make_vjp(f)\n    result, vjp = wrapped_fn(tf.constant(3.0))\n    # result is 9.0\n    vjp()  # the vjp function rturns 6.0\n\n  Raises:\n    ValueError: if `f` returns None.\n  '

    def decorated(*args, **kwds):
        'Computes the value and gradient of the decorated function.'
        parameter_positions = _get_arg_spec(f, params, args)
        assert (not kwds), "The gradient function can't take keyword arguments."
        this_tape = tape.push_new_tape(persistent=persistent)
        try:
            sources = []
            args = [(ops.convert_to_tensor(args[i]) if (i in parameter_positions) else args[i]) for i in range(len(args))]
            args = _ensure_unique_tensor_objects(parameter_positions, args)
            for i in parameter_positions:
                sources.append(args[i])
                tape.watch(this_tape, args[i])
            result = f(*args)
            if (result is None):
                raise ValueError('Cannot differentiate a function that returns None; did you forget to return a value from {}?'.format(f.__name__))
            flat_result = nest.flatten(result)
            flat_result = [gen_array_ops.identity(x) for x in flat_result]
            result = nest.pack_sequence_as(result, flat_result)
        finally:
            tape.pop_tape(this_tape)

        def vjp(dy=None):
            if (dy is not None):
                dy = [ops.convert_to_tensor(x) for x in nest.flatten(dy)]
            return imperative_grad.imperative_grad(this_tape, nest.flatten(result), sources, output_gradients=dy)
        return (result, vjp)
    return decorated
