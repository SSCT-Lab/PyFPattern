def get_payload_from_parameters(params):
    payload = {
        
    }
    for parameter in params:
        parameter_value = params[parameter]
        if (parameter_value and is_checkpoint_param(parameter)):
            if isinstance(parameter_value, dict):
                payload[parameter.replace('_', '-')] = get_payload_from_parameters(parameter_value)
            else:
                payload[parameter.replace('_', '-')] = parameter_value
    return payload