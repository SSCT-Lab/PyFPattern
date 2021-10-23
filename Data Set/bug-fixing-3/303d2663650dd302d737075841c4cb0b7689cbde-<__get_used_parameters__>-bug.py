def __get_used_parameters__(layer_names):
    parameter_names = set()
    for name in layer_names:
        l = cp.g_layer_map[name]
        for inp in l.inputs:
            if inp.input_parameter_name:
                parameter_names.add(inp.input_parameter_name)
        if l.bias_parameter_name:
            parameter_names.add(l.bias_parameter_name)
    return parameter_names