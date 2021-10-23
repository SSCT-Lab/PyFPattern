def check_valid_modification(module, values, modifiable_params):
    ' Check if the parameters and values in values are valid.  '
    changed_with_update = False
    for parameter in values:
        new_value = values[parameter]
        if (parameter not in modifiable_params):
            module.fail_json(msg=('%s is not a modifiable parameter. Valid parameters to modify are: %s.' % (parameter, modifiable_params.keys())))
        str_to_type = {
            'integer': int,
            'string': text_type,
        }
        if (not isinstance(new_value, str_to_type[modifiable_params[parameter][1]])):
            module.fail_json(msg=('%s (type %s) is not an allowed value for the parameter %s. Expected a type %s.' % (new_value, type(new_value), parameter, modifiable_params[parameter][1])))
        if ((text_type(new_value) not in modifiable_params[parameter][0]) and (not isinstance(new_value, int))):
            module.fail_json(msg=('%s is not an allowed value for the parameter %s. Valid parameters are: %s.' % (new_value, parameter, modifiable_params[parameter][0])))
        if (text_type(new_value) != modifiable_params[parameter][2]):
            changed_with_update = True
    return changed_with_update