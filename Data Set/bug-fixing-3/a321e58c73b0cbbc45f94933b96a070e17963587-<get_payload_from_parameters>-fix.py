def get_payload_from_parameters(params):
    payload = {
        
    }
    for parameter in params:
        parameter_value = params[parameter]
        if (parameter_value and is_checkpoint_param(parameter)):
            if isinstance(parameter_value, dict):
                payload[parameter.replace('_', '-')] = get_payload_from_parameters(parameter_value)
            elif (isinstance(parameter_value, list) and (len(parameter_value) != 0) and isinstance(parameter_value[0], dict)):
                payload_list = []
                for element_dict in parameter_value:
                    payload_list.append(get_payload_from_parameters(element_dict))
                payload[parameter.replace('_', '-')] = payload_list
            else:
                payload[parameter.replace('_', '-')] = parameter_value
    return payload