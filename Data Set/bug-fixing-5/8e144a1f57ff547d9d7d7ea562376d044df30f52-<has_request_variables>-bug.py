def has_request_variables(view_func):
    num_params = view_func.__code__.co_argcount
    if (view_func.__defaults__ is None):
        num_default_params = 0
    else:
        num_default_params = len(view_func.__defaults__)
    default_param_names = view_func.__code__.co_varnames[(num_params - num_default_params):]
    default_param_values = view_func.__defaults__
    if (default_param_values is None):
        default_param_values = []
    post_params = []
    for (name, value) in zip(default_param_names, default_param_values):
        if isinstance(value, REQ):
            value.func_var_name = name
            if (value.post_var_name is None):
                value.post_var_name = name
            post_params.append(value)
        elif (value == REQ):
            post_var = value(name)
            post_var.func_var_name = name
            post_params.append(post_var)

    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        for param in post_params:
            if (param.func_var_name in kwargs):
                continue
            if (param.argument_type == 'body'):
                try:
                    val = ujson.loads(request.body)
                except ValueError:
                    raise JsonableError('Malformed JSON')
                kwargs[param.func_var_name] = val
                continue
            elif (param.argument_type is not None):
                raise Exception('Invalid argument type')
            default_assigned = False
            try:
                val = request.REQUEST[param.post_var_name]
            except KeyError:
                if (param.default is REQ.NotSpecified):
                    raise RequestVariableMissingError(param.post_var_name)
                val = param.default
                default_assigned = True
            if ((param.converter is not None) and (not default_assigned)):
                try:
                    val = param.converter(val)
                except JsonableError:
                    raise
                except:
                    raise RequestVariableConversionError(param.post_var_name, val)
            if ((param.validator is not None) and (not default_assigned)):
                try:
                    val = ujson.loads(val)
                except:
                    raise JsonableError(('argument "%s" is not valid json.' % (param.post_var_name,)))
                error = param.validator(param.post_var_name, val)
                if error:
                    raise JsonableError(error)
            kwargs[param.func_var_name] = val
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func