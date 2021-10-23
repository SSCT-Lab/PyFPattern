def _graph_mode_decorator(f, *args, **kwargs):
    'Implement custom gradient decorator for graph mode.'
    if kwargs:
        raise ValueError('The custom_gradient decorator currently supports keywords arguments only when eager execution is enabled.')
    name = ('CustomGradient-%s' % ops.uid())
    args = [ops.convert_to_tensor(x) for x in args]
    current_var_scope = variable_scope.get_variable_scope()
    before_vars = set((current_var_scope.global_variables() + current_var_scope.local_variables()))
    with backprop.GradientTape() as tape:
        (result, grad_fn) = f(*args)
    after_vars = set((current_var_scope.global_variables() + current_var_scope.local_variables()))
    new_vars = (after_vars - before_vars)
    for v in new_vars:
        if (not resource_variable_ops.is_resource_variable(v)):
            raise TypeError('All variables used by a function wrapped with @custom_gradient must be `ResourceVariable`s. Ensure that no `variable_scope` is created with `use_resource=False`.')
    variables = list((set(tape.watched_variables()) - set(args)))
    grad_argspec = tf_inspect.getfullargspec(grad_fn)
    variables_in_signature = (('variables' in grad_argspec.args) or grad_argspec.varkw)
    if (variables and (not variables_in_signature)):
        raise TypeError("If using @custom_gradient with a function that uses variables, then grad_fn must accept a keyword argument 'variables'.")
    if (variables_in_signature and (not variables)):
        if (not variable_scope.get_variable_scope().use_resource):
            raise TypeError('If using @custom_gradient with a function that uses variables, the enclosing variable scope must have use_resource=True.')
        else:
            logging.warn("@custom_gradient grad_fn has 'variables' in signature, but no ResourceVariables were used on the forward pass.")
    flat_result = nest.flatten(result)
    flat_result_len = len(flat_result)
    all_tensors = ((flat_result + args) + variables)

    def tape_grad_fn(*result_grads):
        'Custom grad fn wrapper.'
        result_grads = result_grads[:flat_result_len]
        if variables:
            (input_grads, variable_grads) = grad_fn(*result_grads, variables=variables)
            if (len(variable_grads) != len(variables)):
                raise ValueError('Must return gradient for each variable from @custom_gradient grad_fn.')
        else:
            input_grads = grad_fn(*result_grads)
            variable_grads = []
        input_grads = nest.flatten(input_grads)
        return ((([None] * flat_result_len) + input_grads) + variable_grads)

    @ops.RegisterGradient(name)
    def internal_grad_fn(unused_op, *result_grads):
        'Custom grad fn wrapper.'
        return tape_grad_fn(*result_grads)
    original_tensors = all_tensors
    with ops.get_default_graph().gradient_override_map({
        'IdentityN': name,
    }):
        all_tensors = array_ops.identity_n(all_tensors)
    original_tensors = [ops.convert_to_tensor(x) for x in original_tensors]
    for (i, t) in enumerate(original_tensors):
        if ((t.dtype == dtypes.resource) and hasattr(t, '_handle_data')):
            all_tensors[i]._handle_data = t._handle_data
    tape_lib.record_operation(f.__name__, all_tensors, original_tensors, tape_grad_fn)
    for (ot, t) in zip(original_tensors, all_tensors):
        copy_handle_data(ot, t)
    return nest.pack_sequence_as(structure=result, flat_sequence=all_tensors[:flat_result_len])